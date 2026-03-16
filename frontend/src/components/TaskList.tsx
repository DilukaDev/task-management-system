import React, { useState } from "react";
import type { Task } from "../types/Task";
import { taskService } from "../services/taskService";

interface TaskListProps {
  tasks: Task[];
  onTaskCompleted: () => void;
  isLoading: boolean;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskCompleted,
  isLoading,
}) => {
  const [completingId, setCompletingId] = useState<number | null>(null);

  const handleCompleteTask = async (id: number) => {
    setCompletingId(id);
    try {
      await taskService.completeTask(id);
      onTaskCompleted();
    } catch (error) {
      console.error("Failed to complete task:", error);
    } finally {
      setCompletingId(null);
    }
  };

  return (
    <div
      className="col-md-6 p-5 overflow-auto"
      style={{ maxHeight: "100vh", backgroundColor: "#f4f6f8" }}
    >
      <h2 className="mb-4 fw-bold text-dark">Tasks</h2>
      <div className="d-flex flex-column gap-3">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="card border-0 shadow-sm"
            style={{
              backgroundColor: "#e9ecef",
              borderRadius: "12px",
              transition: "opacity 0.3s ease, transform 0.3s ease",
              opacity: completingId === task.id ? 0.5 : 1,
            }}
          >
            <div className="card-body d-flex justify-content-between align-items-center p-4">
              <div className="pe-4 overflow-hidden">
                <h5 className="card-title fw-bold text-dark mb-1 text-truncate">
                  {task.title}
                </h5>
                <p className="card-text text-secondary mb-0 text-truncate">
                  {task.description}
                </p>
              </div>
              <button
                className="btn btn-outline-success fw-bold flex-shrink-0"
                onClick={() => handleCompleteTask(task.id)}
                disabled={isLoading || completingId === task.id}
                style={{ borderRadius: "8px" }}
              >
                Done
              </button>
            </div>
          </div>
        ))}
        {tasks.length === 0 && !isLoading && (
          <div className="text-center mt-5 text-secondary">
            <h5>No pending tasks.</h5>
          </div>
        )}
      </div>
    </div>
  );
};
