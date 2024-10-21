<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-form @submit.prevent="addGroup">
          <v-text-field
            v-model="newGroupName"
            label="Group Name"
            required
          ></v-text-field>
          <v-btn type="submit" color="primary">Add Group</v-btn>
        </v-form>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-list>
          <v-list-item
            v-for="group in groups"
            :key="group.id"
          >
            <v-list-item-content>{{ group.name }}</v-list-item-content>
            <v-list-item-action>
              <v-btn color="primary" @click="deleteGroup(group.id)">
                <v-icon>mdi-delete</v-icon>
                Delete
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "GroupView",
  data() {
    return {
      newGroupName: "",
      groups: [],
      selectedGroup: null,
    };
  },
  methods: {
    async fetchGroups() {
      console.log("Fetching groups");
      try {
        const response = await this.axios.get(`${this.$store.state.urls.group}/`);
        this.groups = response.data;
        console.log("Fetched groups:", this.groups);
      } catch (error) {
        console.error("Error fetching groups:", error);
      }
    },
    async addGroup() {
      try {
        const response = await this.axios.post(`${this.$store.state.urls.group}/`, {
          name: this.newGroupName,
        });
        if (response.status === 201) {
          this.newGroupName = "";
          this.fetchGroups();
        } else {
          console.error("Error adding group:", response.statusText);
        }
      } catch (error) {
        console.error("Error adding group:", error);
      }
    },
    async deleteGroup(groupId) {
      try {
        const response = await this.axios.delete(`${this.$store.state.urls.group}/${groupId}/`);
        if (response.status === 204) {
          this.fetchGroups();
        } else {
          console.error("Error deleting group:", response.statusText);
        }
      } catch (error) {
        console.error("Error deleting group:", error);
      }
    },
  },
  created() {
    this.fetchGroups();
  },
};
</script>

<style scoped>
.v-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>