from app.schemas.task import TaskCreate

def calculate_priority(task: TaskCreate) -> dict:
    explanation = []

    importance = task.importance if task.importance is not None else 5     # from 1 to 10
    importance_score = (importance/10)*35
    explanation.append(f"Importance level {importance} gives {importance_score:.1f} points")

    if task.deadline_days==0:
        urgency_score = 40
    elif task.deadline_days<=2:
        urgency_score = 35
    elif task.deadline_days<=5:
        urgency_score = 25
    elif task.deadline_days<=10:
        urgency_score = 15
    else:
        urgency_score = 5

    explanation.append(f"Deadline in {task.deadline_days} days gives {urgency_score} urgency points")

    # let's say we have 8 working hours per day to calculate effort score
    available_hours = task.deadline_days*8

    if available_hours-task.estimated_hours<=8:
        effort_score = 25
        explanation.append("Task is feasible within available time")
    elif available_hours-task.estimated_hours<=15:
        effort_score = 20
        explanation.append("Task is tight but still feasible")
    elif available_hours-task.estimated_hours<=20:
        effort_score = 15
        explanation.append("Task is challenging to complete before deadline")
    elif available_hours-task.estimated_hours<=30:
        effort_score = 10
        explanation.append("Task is not realistically completable before deadline")
    else:
        # assigning 30% panelty
        if available_hours<task.estimated_hours:
            effort_score-=0.3*(min(5, task.estimated_hours-available_hours))
            explanation.append("Panelty applied for tasks that exceed available hours")
        else:
            effort_score = 5
            explanation.append("Task is mostly having lower priority due to long deadline and low effort")
        

    total_score = importance_score+urgency_score+effort_score
    # total_score = max(0, min(100, round(total_score)))

    if total_score>=70:
        category = "High Priority"
    elif total_score>=40:
        category = "Medium Priority"
    else:
        category = "Low Priority"

    return {
        "task_id": task.task_id,
        "title": task.title,
        "score": total_score,
        "category": category,
        "explanation": explanation
    }
