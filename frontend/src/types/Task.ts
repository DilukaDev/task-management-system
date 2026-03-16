export interface Task {
  id: number;
  title: string;
  description: string;
  is_completed: boolean;
  created_at: string;
}

export interface TaskCreatePayload {
  title: string;
  description: string;
}
