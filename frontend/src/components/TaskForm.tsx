import React, { useState } from "react";
import { taskService } from "../services/taskService";

interface TaskFormProps {
  onTaskCreated: () => void;
}

export const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      await taskService.createTask({ title, description });
      setTitle("");
      setDescription("");
      onTaskCreated();
    } catch (error) {
      console.error("Failed to add task:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="col-md-6 p-5 border-end"
      style={{ borderColor: "#e2e8f0", backgroundColor: "#ffffff" }}
    >
      <h2 className="mb-4 fw-bold text-dark">Add a Task</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="taskTitle"
            className="form-label fw-semibold text-secondary"
          >
            Title
          </label>
          <input
            type="text"
            className="form-control bg-light"
            id="taskTitle"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={isLoading}
            style={{ border: "1px solid #dee2e6" }}
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="taskDesc"
            className="form-label fw-semibold text-secondary"
          >
            Description
          </label>
          <textarea
            className="form-control bg-light"
            id="taskDesc"
            rows={5}
            placeholder="Add some details..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isLoading}
            style={{ border: "1px solid #dee2e6" }}
          ></textarea>
        </div>
        <div className="d-flex justify-content-end">
          <button
            type="submit"
            className="btn btn-primary px-5 shadow-sm fw-bold border-0"
            style={{ backgroundColor: "#0d6efd" }}
            disabled={isLoading}
          >
            Add
          </button>
        </div>
      </form>
    </div>
  );
};
