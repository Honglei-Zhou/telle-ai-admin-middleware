### Telle AI Client Middleware

### Description 
This project is part of Telle AI Chatbot System. The client middleware is dealing with chatbot side Socket Connection.

### Interfaces/APIs

#### 1. From Client Server to Chatbot
```buildoutcfg

socket-channel: MUTE_STATE
message type: dictionary
message: {'type': 'MUTE_STATUS',
          'dealerId': dealerId,
          'groupId': groupID, 
          'adminId': adminId,
          'muted': True|False}

socket-channel: CLOSE_CHAT
message type: dictionary
message: {'type': 'CLOSE_CHAT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': admin_id,
          'user': 'admin',
          'close': True
         }

socket-channel: CHAT_MESSAGE
message type: dictionary
message: {'type': 'CHAT_MSG', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId, # required if user is admin
          'user': 'customer|admin|bot',
          'muted': True|False,
          'unread': 0,
          'message': message
         }
         
socket-channel: SYS_MESSAGE
message type: dictionary
message: {'type': 'SYS_MSG', 
          'dealerId': dealerId,
          'adminId': adminId,
          'user': 'admin',
          'muted': True,
          'unread': 0,
          'message': message
         }
```

#### 2. From Chatbot to Client Server
```buildoutcfg

socket-channel: customer_message
message type: dictionary
message: {'type': 'UPDATE_MSG', 
          'dealerId': dealerId,
          'groupId': groupId,
          'user': 'customer',
          'adminId': adminId,
          'muted': True|False
          'unread': 0,
          'message': message
         }

socket-channel: client_join
message type: dictionary
message: {'type': 'CLIENT_JOIN', 
          'dealerId': dealerId,
          'groupId': groupId,
          'user': 'customer',
          'online': True
         }
         
```

#### 3. From other servers by redis channel to Client Server
```buildoutcfg

message type: dictionary
message: {'type': 'UPDATE_MSG', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId, # required if user is admin
          'user': 'admin|customer|bot',
          'muted': True|False,
          'unread': 0,
          'message': message
         }

message type: dictionary
message: {'type': 'MUTE_BOT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId,
          'muted': True
         }

message type: dictionary
message: {'type': 'UNMUTE_BOT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId,
          'muted': False
         }
          
message type: dictionary
message: {'type': 'CLOSE_CHAT', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId,
          'close': True
         }
```
