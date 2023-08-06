Sapi makes creating Virtual Assistant very simple. Sapi uses the pyttsx3 engine to function

Here are some functions:

    speak():
        speak() allows you to make your Virtual Assistant talk.
        Example:
        speak('Hello, World')

    create():
        create() allows you to make a file with your Virtual Assistant voice.
        Example:
        speak('Hello, World', 'test.mp4')
    
    set_rate():
        set_rate() allows you to set the rate your Virtual Assistant voice.
        Example:
        set_rate(125)

    set_volume():
        set_volume() allows you to set the volume your Virtual Assistant voice.
        Example:
        set_volume(1.0)

    set_gender():
        set_gender() allows you to set the voice your Virtual Assistant.
        Example:
        set_gender(voices[1].id) for a female voice
        set_gender(voices[0].id) for a male voice
