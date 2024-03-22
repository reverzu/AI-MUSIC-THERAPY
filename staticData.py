music_quotes = [
    """Music expresses that which cannot be said and on which it is impossible to be silent." - Victor Hugo""",
    """Music washes away from the soul the dust of everyday life." - Berthold Auerbach""",
    """Without music, life would be a mistake." - Friedrich Nietzsche""",
    """Music is the strongest form of magic." - Franz Liszt""",
    """If music be the food of love, play on." - William Shakespeare""",
    """After silence, that which comes nearest to expressing the inexpressible is music." - Aldous Huxley""",
    """The cool thing about music is that no one can take music away from you, writing-wise." - Ray Charles""",
    """Where words fail, music speaks." - Hans Christian Andersen"""
]

articles_dict = {
    """Music's Magical Melody: How Music Therapy Soothes the Soul""": ["""This article explores the scientific underpinnings of music therapy, delving into how music's rhythm, melody, and harmony impact our brain and emotions. It showcases real-life stories of individuals who found solace and healing through music therapy.""", f'https://us.sagepub.com/en-us/nam/node/7006/print'],
    """From Nursery Rhymes to Rehabs: The Diverse Applications of Music Therapy""": ["""This piece tackles the misconception that music therapy is just for relaxation. It highlights its diverse applications, from helping children with developmental delays to aiding in pain management for patients undergoing surgery.""", f'https://www.musictherapy.org/'],
    """Unleashing the Inner Musician: Music Therapy as a Tool for Self-Expression""": ["""This article focuses on the empowering aspect of music therapy, showcasing how it can unlock hidden potential and provide a safe space for individuals to express themselves creatively. It explores methods like songwriting and improvisation as therapeutic tools.""", f'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9286888/'],
    """Beyond Notes and Chords: The Healing Power of Music Listening""": ["""This piece expands the scope of music therapy beyond active participation. It explores the therapeutic benefits of simply listening to music, highlighting curated playlists and specific genres that can alleviate anxiety, enhance mood, and improve cognitive function.""", f' https://www.verywellmind.com/'],
    """Music Therapy: A Symphony of Hope for Chronic Conditions""": ["""This article sheds light on the role of music therapy in managing chronic conditions like pain, fatigue, and depression. It showcases how tailored music interventions can improve quality of life for individuals facing long-term health challenges.""", f'https://www.musictherapy.org/about/musictherapy/']
}

def template(context, question):
    return f"""Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Context: {context}
    Question: {question}
    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

pre_prompt = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\nGenerate the response by answering the question as succinctly as possible. If you cannot answer the question, please state that you do not have an answer.\n"""

def prompter(context, question):
    prompt = pre_prompt + f"CONTEXT:\n\n{context}\n" + \
    f"Question : {question}" + "[\INST]"
    return prompt


chats_dict = {
    "What is AI Music Therapy?": "AI Music Therapy is a form of therapy that utilizes artificial intelligence (AI) to create personalized music experiences for individuals with mental health conditions or disabilities. It involves the use of machine learning algorithms and natural language processing to analyze a person's emotional state and generate customized music tracks that can help them relax, reduce anxiety, or improve their mood. AI Music Therapy is still a relatively new field, but it has shown promising results in early studies and has the potential to provide an innovative and effective approach to mental health treatment.", 
    "What is Music Therapy?": """Music therapy is a form of therapy that uses music to help individuals cope with various challenges and issues in their lives. It involves working with a trained music therapist who uses music and music-making techniques to promote emotional healing, social skills development, and cognitive function improvement. Music therapy can be used to treat a wide range of conditions, including mental health disorders, neurological impairments, and physical disabilities. It can also be used to enhance personal growth and well-being.

    Music therapy is based on the belief that music has the power to elicit deep emotional responses and promote healing at a profound level. By working with music, individuals can gain insight into their thoughts, feelings, and behaviors, and develop new coping skills and strategies for managing challenges in their lives.

    Some of the key techniques used in music therapy include:

    Improvisation: creating music spontaneously in the moment to express emotions and experiences
    Composition: writing and recording original songs to express personal experiences and emotions
    Music listening: actively engaging with and responding to pre-recorded music to explore emotions and gain insight into one's self
    Music movement: using music to facilitate physical movements and gestures that can help to release tension, improve coordination, and enhance mood.
    Music therapy is a highly individualized form of therapy, and the specific techniques used will depend on the taste of the individual""", 
    "Is Music Therapy useful?": '''Yes, music therapy has been shown to be a useful tool in improving mental health and well-being. Research has consistently demonstrated its benefits in reducing stress, anxiety, and depression, as well as improving cognitive function and social skills. Music therapy can be particularly helpful for individuals with neurological or psychiatric disorders, such as Alzheimer's disease, dementia, post-traumatic stress disorder (PTSD), and schizophrenia. Additionally, music therapy has been used to help individuals cope with grief, loss, and trauma.

    However, it is important to note that music therapy should be provided by a licensed and trained professional, as improper use of music can have unintended negative consequences. For example, loud or disruptive music can exacerbate anxiety or stress, while inappropriate lyrics can cause emotional distress.

    Overall, music therapy has the potential to be a valuable addition to traditional therapeutic approaches, and its benefits should not be underestimated.'''
}
