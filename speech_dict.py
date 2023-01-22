# Some dictionaries containing scripts for Misty as a healthcare receptionist

# Check in: new patient
script1_dict = {
    "welcome_unknown": {
        "formal": "Good morning, welcome to Doctor Martys practice. How may I be of service?",
        "informal": "Hi! Welcome to Doctor Martys practice. How can I help?"
    },
    "check_appointment_unknown": {
        "formal": "I will check the agenda for you. Would you please state your full name for me?",
        "informal": "Okay, let me check that for you. What is your full name?"
    },
    "confirm_appointment_unknown": {
        "formal": "Yes I can see your appointment at eleven A.M., I will now register you as present. This is your first visit here, is that correct?",
        "informal": "Hi {}, nice to meet you! Is this your first time here?"
    },
    "prompt_health_form": {
        "formal": "Before meeting the doctor I will need you to fill in a health form with me. Please state your date of birth.",
        "informal": "So {}, before you can see doctor Marty, we need to fill in a health form. When were you born?"
    },
    "address": {
        "formal": "What is your current address?",
        "informal": "Okay and where do you live?"
    },
    "contact": {
        "formal": "Please state your phone number and email address.",
        "informal": "Thanks! In case we need to contact you, what are your phone number and email address?"
    },
    "medication": {
        "formal": "Are you aware of any pre-exisitng health conditions you might have?",
        "informal": "Great! Finally, do you suffer from any health problems?"
    },
    "finish_intake": {
        "formal": "Thank you, we have reached the end of the health form. Please take a seat in the waiting room behind you, Doctor Marty will be with you shortly.",
        "informal": "Thank you {}, that is all the questions I have for you. You can sit down in the room behind you and I will let Doctor Marty know you arrived."
    }
}
