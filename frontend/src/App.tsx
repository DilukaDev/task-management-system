import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import type { Task } from "./types/Task";
import { taskService } from "./services/taskService";
import { TaskForm } from "./components/TaskForm";
import { TaskList } from "./components/TaskList";

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTasks = async () => {
    setIsLoading(true);
    try {
      const data = await taskService.getRecentTasks();
      setTasks(data);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleTaskCreated = () => {
    fetchTasks();
  };

  const handleTaskCompleted = () => {
    fetchTasks();
  };

  return (
    <div
      className="container-fluid min-vh-100 p-0"
      style={{ backgroundColor: "#f4f6f8" }}
    >
      <div className="row g-0 h-100 min-vh-100">
        <TaskForm onTaskCreated={handleTaskCreated} />
        <TaskList
          tasks={tasks}
          onTaskCompleted={handleTaskCompleted}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

export default App;
