from channels.routing import ProtocolTypeRouter, URLRouter
import competition.routing

application = ProtocolTypeRouter({
    'http': URLRouter(competition.routing.urlpatterns),
})
