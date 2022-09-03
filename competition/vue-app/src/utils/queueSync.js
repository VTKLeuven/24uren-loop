class QueueSync {
    constructor(axios, store, oncreate, ondelete) {
        this.queue = [];

        this.updates = [];
        this.lastUpdate = -1;
        this.updateSent = false;

        this.updateTimeout = null;
        this.queueRefreshDelay = 5000;
        this.loading = true;

        this.axios = axios;
        this.$store = store;
        this.oncreate = oncreate || (() => {});
        this.ondelete = ondelete || (() => {});
    }

    /* ========================================================================================================= */
    /* == Initialization and destruction == */
    async init() {
        /* Refresh queue data */
        await this.refresh();

        /* Subscribe to the sse events */
        await this.$store.dispatch('subscribe_sse', {event: 'queue_update', handler: this.onQueueUpdate.bind(this)});
        await this.$store.dispatch('subscribe_sse', {event: 'queue_delete', handler: this.onQueueDelete.bind(this)});
        await this.$store.dispatch('subscribe_sse', {event: 'queue_soft_delete', handler: this.onQueueSoftDelete.bind(this)});
        await this.$store.dispatch('subscribe_sse', {event: 'queue_move', handler: this.onQueueMove.bind(this)});
        await this.$store.dispatch('subscribe_sse', {event: 'queue_insert', handler: this.onQueueInsert.bind(this)});
    }

    async refresh() {
        this.queue = [];
        this.loading = true;
        /* Initialized the queue data */
        await this.getLastUpdateId();
        await this.refreshQueue();
        this.loading = false;
    }

    destroy() {
        /* Unsubscribe from sse events */
        this.$store.dispatch('unsubscribe_sse', {event: 'queue_update', handler: this.onQueueUpdate.bind(this)});
        this.$store.dispatch('unsubscribe_sse', {event: 'queue_delete', handler: this.onQueueDelete.bind(this)});
        this.$store.dispatch('unsubscribe_sse', {event: 'queue_soft_delete', handler: this.onQueueSoftDelete.bind(this)});
        this.$store.dispatch('unsubscribe_sse', {event: 'queue_move', handler: this.onQueueMove.bind(this)});
        this.$store.dispatch('unsubscribe_sse', {event: 'queue_insert', handler: this.onQueueInsert.bind(this)});
    }

    async getLastUpdateId() {
        /* Retrieve the update counter */
        let resp = await this.axios.get(`${this.$store.state.urls.counter}/`, {params: {name: 'queue_op'}});
        this.lastUpdate = resp.data[0].count;
    }

    async refreshQueue() {
        /* Load the queue */
        let resp = await this.axios.get(`${this.$store.state.urls.queue_ticket}/`,
            {
                params: {
                    deleted: false,
                    ran: false
                }
            });
        /* Add a key to each queue item */
        let queue = resp.data;
        queue.forEach(this.oncreate);
        this.queue = queue;
    }

    onQueueUpdate(resp) {this.onQueueSSEEvent(resp, 'update')}
    onQueueDelete(resp) {this.onQueueSSEEvent(resp, 'delete')}
    onQueueSoftDelete(resp) {this.onQueueSSEEvent(resp, 'soft-delete')}
    onQueueMove(resp) {this.onQueueSSEEvent(resp, 'move')}
    onQueueInsert(resp) {this.onQueueSSEEvent(resp, 'insert')}
    /* ========================================================================================================= */

    /* ========================================================================================================= */
    /* == Event updates == */
    onQueueSSEEvent(resp, type) {
        let update = JSON.parse(resp.data);

        /* Queue incoming updates when this user sent an update */
        if (this.lastUpdate === update.id && !this.updateSent) {
          this.applyUpdate(type, update);
          this.applyQueuedUpdates();
        } else if (this.lastUpdate < update.id || this.updateSent) {
          this.addUpdate(type, update);
        }
    }

    applyUpdate(type, update) {
        this.applyData(type, update.data);
        this.lastUpdate++;
    }

    applyQueuedUpdates() {
        /* Clear refresh timer */
        if (this.updateTimeout !== null) {
            clearTimeout(this.updateTimeout);
            this.updateTimeout = null;
        }

        /* Perform updates */
        this.updates.sort((a, b) => a.id - b.id);
        let i;
        for (i = 0; i < this.updates.length; ++i) {
            let update = this.updates[i];
            if (update.id < this.lastUpdate) continue;
            if (update.id === this.lastUpdate)
                this.applyUpdate(update.type, update.data);
        }
        this.updates.splice(0, i);

        /* Set new timer if not all updates were applied */
        if (this.updates.length > 0) this.updateTimeout = setTimeout(this.refresh.bind(this), this.queueRefreshDelay);
    }

    addUpdate(type, update) {
        if (this.updates.filter(el => el.id === update.id).length === 0) {
            this.updates.push({type: type, data: update});
            if (this.updateTimeout === null) this.updateTimeout = setTimeout(this.refresh.bind(this), this.queueRefreshDelay);
        }
      }

    async sendUpdate(type, data) {
        this.updateSent = true;
        let update = {id: this.lastUpdate, data: data};
        let result;

        /* Send the update */
        switch (type) {
            case 'move':
                /* Perform the movement in data */
                this.applyData('move', data);
                result = this.axios.post(`${this.$store.state.urls.queue_move}/`, update).then(resp => {
                    let success = resp.data.success;
                    if (!success) {
                        this.applyData('move', {pos_move: update.data.pos_target, pos_target: update.data.pos_move});
                        this.lastUpdate--;
                    }
                    return success;
                });
                break;
            case 'delete':
                this.applyData('soft-delete', data)
                result = this.axios.delete(`${this.$store.state.urls.queue_ticket}/${update.data.id}/`,{data: update}).then(resp => {
                    let success = resp.data.success;
                    if (!success) {
                        this.applyData('insert', {pos: update.data.id, ticket: update.data});
                        this.lastUpdate--;
                    }
                    return success;
                });
                break;
            default:
                console.log('Unknown type', type, 'in sendUpdate');
        }

        /* Clear once the update has come through */
        result.then((success) => {
            this.updateSent = false;
            this.applyQueuedUpdates();
            return success;
        })

        /* Increase the update by one */
        this.lastUpdate++;
        return result;
    }
    /* ========================================================================================================= */

    /* ========================================================================================================= */
    /* == Queue transformations == */
    applyData(type, data) {
        switch(type) {
          case 'update':
            this.queueUpdateData(data);
            break;
          case 'delete':
          case 'soft-delete':
            this.queueDeleteData(data);
            break;
          case 'move':
            this.queueMoveData(data);
            break;
          case 'insert':
            this.queueInsertData(data);
            break;
        }
    }
    queueUpdateData(data) {
        /* data = {id: <>, runner: <>, registration_time: <>, deleted: <>, ran: <>} */

        /* Simple update to a queue element */
        let ticketIndex = this.queue.findIndex(el => el.id === data.id);
        /* If a ticket is found, update it, otherwise add the new ticket */
        if (ticketIndex !== -1) {
            if (data.deleted || data.ran) {
                this.queueDeleteData({id: data.id});
            } else {
                data.key = this.queue[ticketIndex].key;
                this.queue.splice(ticketIndex, 1, data);
            }
        } else {
            /* Find the index of the first ticket that has a higher id (being later in the queue) */
            let i = this.queue.findIndex(el => el.id > data.id);
            if (i === -1) i = this.queue.length;
            this.queueInsertData({pos: i, ticket: data});
        }
    }
    queueDeleteData(data) {
        /* data = {id: <>} */
        let i = this.queue.findIndex(el => el.id === data.id);
        let ticket = this.queue.splice(i, 1);
        this.ondelete(ticket);

        // this.queue = this.queue.filter(el => el.id !== data.id);
    }
    queueMoveData(data) {
        /* data = {pos_move: <>, pos_target: <>} */
        this._move(data.pos_move, data.pos_target);
    }
    queueInsertData(data) {
        /* data = {pos: <>, ticket: <>} */
        this.oncreate(data.ticket);
        this.queue.splice(data.pos, 0, data.ticket);
    }
    _move(from, to) {
        /* Move the element */
        this.queue.splice(to, 0, this.queue.splice(from, 1)[0]);

        /* Edit the indices */
        let id = this.queue[to].id;
        if (from > to) {
            for (let i = to; i < from; ++i) {
                this.queue[i].id = this.queue[i + 1].id;
            }
        } else {
            for (let i = to; i > from; --i) {
                this.queue[i].id = this.queue[i - 1].id;
            }
        }
        this.queue[from].id = id;

    }

      /* ========================================================================================================= */
}

export {QueueSync}