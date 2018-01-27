from channels import include

channel_routing = [
    include("chat.routing.channel_routing", path=r"^/chat/"),
    include("chat.routing.custom_routing")
]
