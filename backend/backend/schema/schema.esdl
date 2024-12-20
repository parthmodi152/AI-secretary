module default {
    type Caller {
        required property phone_number -> str {
            constraint exclusive;
        };
        required property first_interaction -> datetime;
        required property last_interaction -> datetime;
        multi link conversations -> Conversation;
    }

    type Conversation {
        required property timestamp -> datetime;
        required property importance_level -> str;
        required property summary -> str;
        required property action_taken -> str;
        required link caller -> Caller;
    }
} 