"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Header } from "@/components/header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Todo {
  id: string;
  title: string;
  content?: string;
  completed: boolean;
  owner_id: string;
}

export default function Page() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");

  const fetchTodos = async () => {
    setLoading(true);
    try {
      const response = await axios.get<Todo[]>("http://localhost:8000/todo", {
        withCredentials: true,
      });
      setTodos(response.data);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || err.message || "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const addTodo = async () => {
    if (!newTitle) return;

    try {
      const response = await axios.post<Todo>(
        "http://localhost:8000/todo",
        {
          title: newTitle,
          content: newContent,
          completed: false,
        },
        { withCredentials: true }
      );

      setTodos((prev) => [...prev, response.data]);
      setNewTitle("");
      setNewContent("");
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || "Failed to add todo");
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await axios.delete(`http://localhost:8000/todo/${id}`, {
        withCredentials: true,
      });
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err: any) {
      alert(
        err.response?.data?.detail || err.message || "Failed to delete todo"
      );
    }
  };

  const toggleComplete = async (todo: Todo) => {
    try {
      const response = await axios.patch<Todo>(
        `http://localhost:8000/todo/${todo.id}`,
        { completed: !todo.completed },
        {
          withCredentials: true,
        }
      );
      setTodos((prev) =>
        prev.map((t) => (t.id === todo.id ? response.data : t))
      );
    } catch (err: any) {
      alert(
        err.response?.data?.detail || err.message || "Failed to update todo"
      );
    }
  };

  return (
    <div className="w-full h-full">
      <Header />
      <div className="flex flex-col items-center justify-start py-16 px-4">
        <h1 className="text-4xl font-bold text-black dark:text-zinc-50 mb-8">
          Todo App
        </h1>

        {/* New Todo Form */}
        <div className="mb-8 flex w-full max-w-md flex-col gap-2">
          <Input
            type="text"
            placeholder="Todo title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />
          <Input
            type="text"
            placeholder="Todo content"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
          />
          <Button onClick={addTodo}>Add Todo</Button>
        </div>

        {/* Todo List */}
        <div className="flex flex-col w-full max-w-md gap-4">
          {loading && (
            <p className="text-black dark:text-zinc-50">Loading...</p>
          )}
          {error && <p className="text-red-500">{error}</p>}

          {todos.map((todo) => (
            <div
              key={todo.id}
              className="flex justify-between items-center p-4 border rounded-md bg-white dark:bg-gray-900"
            >
              <div>
                <h2
                  className={`font-bold text-lg ${
                    todo.completed
                      ? "line-through text-gray-400"
                      : "text-black dark:text-zinc-50"
                  }`}
                >
                  {todo.title}
                </h2>
                <p
                  className={`${
                    todo.completed
                      ? "line-through text-gray-400"
                      : "text-gray-600 dark:text-gray-300"
                  }`}
                >
                  {todo.content}
                </p>
              </div>
              <div className="flex gap-2">
                <Button onClick={() => toggleComplete(todo)}>
                  {todo.completed ? "Undo" : "Complete"}
                </Button>
                <Button
                  onClick={() => deleteTodo(todo.id)}
                  variant="destructive"
                >
                  Delete
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
