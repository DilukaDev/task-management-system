import axios from "axios";
import type { Task, TaskCreatePayload } from "../types/Task";
import { API_BASE_URL } from "../config/config";

const taskApi = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
});

export const taskService = {
  getRecentTasks: async (): Promise<Task[]> => {
    try {
      const response = await taskApi.get<Task[]>("/tasks/recent");
      return response.data;
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
      throw error;
    }
  },

  createTask: async (payload: TaskCreatePayload): Promise<Task> => {
    try {
      const response = await taskApi.post<Task>("/tasks/create", payload);
      return response.data;
    } catch (error) {
      console.error("Failed to create task:", error);
      throw error;
    }
  },

  completeTask: async (taskId: number): Promise<Task> => {
    try {
      const response = await taskApi.patch<Task>(`/tasks/${taskId}/complete`);
      return response.data;
    } catch (error) {
      console.error("Failed to complete task:", error);
      throw error;
    }
  },
};
