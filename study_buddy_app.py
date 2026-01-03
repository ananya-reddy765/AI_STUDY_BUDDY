import tkinter as tk
from tkinter import ttk, messagebox
import json, os
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# ===== GLOBAL VARIABLES =====
scores = {}
subjects_list = ["OS", "Web Tech", "ML", "AI"]

# ===== FILE HANDLING =====
def save_scores():
    with open("scores.json", "w") as f:
        json.dump(scores, f)

def load_scores():
    global scores
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            scores = json.load(f)

# ===== ML PERFORMANCE PREDICTION =====
def ml_predict_performance():
    if not scores:
        return "Not enough data"
    values = [scores.get(sub, 50) for sub in ["OS", "Web Tech", "ML"]]
    X_train = np.array([[30,40,50],[70,80,90],[40,50,60]])
    y_train = ["Weak","Strong","Average"]
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    X_test = np.array([values])
    return clf.predict(X_test)[0]

# ===== QUIZ QUESTIONS =====
questions = {
    "OS":[
        ("Which of these is a type of OS?", ["Batch","HTML","TCP","CSS"], "Batch"),
        ("OS manages?", ["Resources","Web pages","HTML tags","IP addresses"], "Resources"),
        ("Example of process scheduling?", ["Round Robin","CSS styling","IP routing","Hypertext"], "Round Robin"),
        ("What is deadlock?", ["Resource Block","CPU speed","Network error","HTML attribute"], "Resource Block"),
        ("Virtual memory is used for?", ["Storage","Network","AI models","HTML rendering"], "Storage")
    ],
    "Web Tech":[
        ("HTML stands for?", ["Hypertext Markup Language","High Transfer Markup Language","Hyperlink Text Machine","Hyper Text Machine"], "Hypertext Markup Language"),
        ("CSS is used for?", ["Styling","Programming","Networking","AI"], "Styling"),
        ("JS is?", ["A programming language","A database","OS type","HTML tag"], "A programming language"),
        ("HTTP stands for?", ["Hypertext Transfer Protocol","High Transfer Text Program","Hyperlink Text Protocol","Hyper Transfer Tag Protocol"], "Hypertext Transfer Protocol"),
        ("Tag for link in HTML?", ["<a>","<p>","<img>","<div>"], "<a>")
    ],
    "ML":[
        ("ML stands for?", ["Machine Logic","Machine Learning","Manual Learning","Modern Language"], "Machine Learning"),
        ("ML is a subset of?", ["Data Science","AI","OS","Web Tech"], "AI"),
        ("Supervised learning uses?", ["Labeled data","Unlabeled data","Random data","No data"], "Labeled data"),
        ("Unsupervised learning uses?", ["Labeled data","Unlabeled data","Structured data","None"], "Unlabeled data"),
        ("ML learns from?", ["Code","Data","Hardware","Users"], "Data")
    ],
    "AI":[
        ("AI stands for?", ["Automatic Instruction","Artificial Intelligence","Advanced Internet","Algorithmic Interface"], "Artificial Intelligence"),
        ("AI is mainly used for?", ["Making machines intelligent","Operating systems","Web design","Networking"], "Making machines intelligent"),
        ("Which is a type of AI?", ["Narrow AI","Wide AI","Medium AI","Small AI"], "Narrow AI"),
        ("AI applications include?", ["Chatbots","Operating systems","HTML pages","Memory management"], "Chatbots"),
        ("Machine Learning is part of AI?", ["True","False"], "True")
    ]
}

# ===== ACTIVE QUIZ (MCQ BUTTON STYLE) =====
def start_quiz():
    subject = quiz_subject_var.get()
    if subject == "":
        messagebox.showerror("Error", "Select a subject first")
        return

    qlist = questions[subject]
    quiz_window = tk.Toplevel(app)
    quiz_window.title(f"{subject} Quiz")
    quiz_window.geometry("500x350")
    index = 0
    score = 0

    question_label = tk.Label(quiz_window, text="", font=("Arial",12))
    question_label.pack(pady=20)
    button_frame = tk.Frame(quiz_window)
    button_frame.pack(pady=10)

    progress_label = tk.Label(quiz_window, text="")
    progress_label.pack(pady=10)

    def load_question():
        nonlocal index
        question_label.config(text=f"Q{index+1}: {qlist[index][0]}")
        progress_label.config(text=f"{index+1}/{len(qlist)}")
        for widget in button_frame.winfo_children():
            widget.destroy()
        for opt in qlist[index][1]:
            tk.Button(button_frame, text=opt, width=25, bg="#03A9F4", fg="white",
                      command=lambda choice=opt: submit(choice)).pack(pady=5)

    def submit(choice):
        nonlocal index, score
        if choice == qlist[index][2]:
            score += 10
        index += 1
        if index < len(qlist):
            load_question()
        else:
            final_score = int((score/(len(qlist)*10))*100)
            scores[subject] = final_score
            save_scores()
            bot_message(f"Quiz completed for {subject}. Score: {final_score}")
            quiz_window.destroy()

    load_question()

# ===== STUDY PLAN =====
def generate_plan():
    plan_text.delete("1.0",tk.END)
    plan=""
    for sub in subjects_list:
        if sub in scores:
            if scores[sub]<50:
                plan += f"{sub}: 3 hrs/day (Weak)\n"
            else:
                plan += f"{sub}: 1 hr/day (Strong)\n"
        else:
            plan += f"{sub}: 2 hrs/day (New)\n"
    plan_text.insert(tk.END, plan)

# ===== PERFORMANCE GRAPH =====
def show_graph():
    if not scores:
        messagebox.showinfo("Graph","No scores to display")
        return
    values = [scores.get(sub,0) for sub in subjects_list]
    colors = ["red" if v<50 else "green" for v in values]
    plt.bar(subjects_list, values, color=colors)
    plt.title("Quiz Performance")
    plt.ylabel("Score (%)")
    plt.show()

# ===== CHATBOT =====
def bot_message(msg):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, "AI: "+msg+"\n")
    chat_box.see(tk.END)
    chat_box.config(state="disabled")

def ai_reply():
    user_msg = chat_entry.get().lower()
    chat_entry.delete(0,tk.END)
    chat_box.config(state="normal")
    chat_box.insert(tk.END,"You: "+user_msg+"\n")
    reply=None
    knowledge_base={
        "what is os":"OS is Operating System, it manages hardware and software resources.",
        "what is web tech":"Web Tech includes HTML, CSS, JS used for web development.",
        "what is ml":"Machine Learning allows systems to learn from data.",
        "what is ai":"AI is Artificial Intelligence that makes machines intelligent.",
        "motivate me":"You are doing great. Keep learning and practicing!"
    }
    for key in knowledge_base:
        if key in user_msg:
            reply=knowledge_base[key]
            break
    if reply is None and "predict" in user_msg:
        reply="ML Prediction: "+ml_predict_performance()
    elif reply is None and any(w in user_msg for w in ["hi","hello","hey"]):
        reply="Hello! Ask me about OS, Web Tech, ML, AI, quizzes, or performance."
    elif reply is None and user_msg.startswith("what"):
        reply="That’s a good question. I am still learning this topic."
    elif reply is None:
        reply="I can help with OS, Web Tech, ML, AI quizzes and study plans."
    chat_box.insert(tk.END,"AI: "+reply+"\n")
    chat_box.see(tk.END)
    chat_box.config(state="disabled")

# ===== MAIN GUI =====
load_scores()
app=tk.Tk()
app.title("AI Study Buddy – Interactive GUI")
app.geometry("600x700")

tab_control = ttk.Notebook(app)

# ===== TAB 1: Quiz =====
quiz_tab = ttk.Frame(tab_control)
tab_control.add(quiz_tab, text="Quiz")

quiz_subject_var = tk.StringVar()
tk.Label(quiz_tab, text="Select Subject:",font=("Arial",12)).pack(pady=10)
subject_menu = ttk.Combobox(quiz_tab, values=subjects_list, textvariable=quiz_subject_var)
subject_menu.pack()
tk.Button(quiz_tab,text="Start Quiz",command=start_quiz,bg="#2196F3",fg="white").pack(pady=10)

# ===== TAB 2: Study Plan =====
plan_tab = ttk.Frame(tab_control)
tab_control.add(plan_tab, text="Study Plan")
tk.Button(plan_tab,text="Generate Study Plan",command=generate_plan,bg="#FF5722",fg="white").pack(pady=10)
plan_text = tk.Text(plan_tab,height=10)
plan_text.pack(pady=10)
tk.Button(plan_tab,text="Show Performance Graph",command=show_graph,bg="#4CAF50",fg="white").pack(pady=10)

# ===== TAB 3: Chatbot =====
chat_tab = ttk.Frame(tab_control)
tab_control.add(chat_tab,text="Chatbot")
chat_box = tk.Text(chat_tab,height=15,state="disabled")
chat_box.pack(pady=10)
chat_entry = tk.Entry(chat_tab,width=50)
chat_entry.pack(side=tk.LEFT,padx=5)
tk.Button(chat_tab,text="Send",command=ai_reply,bg="#9C27B0",fg="white").pack(side=tk.LEFT)

tab_control.pack(expand=1,fill="both")
bot_message("Hello! I am your AI Study Buddy 🤖")

app.mainloop()
