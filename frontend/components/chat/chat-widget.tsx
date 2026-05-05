"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import api from "@/lib/api";
import { X, Send, Bot, User, ShoppingBag } from "lucide-react";
import { Product } from "@/lib/types";
import { formatPrice } from "@/lib/utils";
import Link from "next/link";

interface ChatResponse {
  response: string;
  session_id: string;
  intent?: string;
  suggested_products?: Product[];
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string>("");

  const sendMessage = useMutation({
    mutationFn: async (message: string) => {
      const response = await api.post("/chat/", {
        message,
        session_id: sessionId || undefined,
      });
      return response.data as ChatResponse;
    },
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        { role: "user", content: input },
        { role: "assistant", content: data.response },
      ]);
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }
      setInput("");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage.mutate(input);
  };

  return (
    <>
      {/* Chat Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-blue-700 transition-all z-50 ${
          isOpen ? "hidden" : "block"
        }`}
      >
        <Bot className="w-7 h-7" />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[32rem] bg-white rounded-xl shadow-2xl flex flex-col z-50">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-xl flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Bot className="w-6 h-6" />
              <span className="font-semibold">AI Assistant</span>
            </div>
            <button onClick={() => setIsOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <Bot className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p>Xin chào! Tôi có thể giúp gì cho bạn?</p>
                <p className="text-sm mt-2">
                  Hỏi về sản phẩm, giá cả, hoặc cách đặt hàng nhé!
                </p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            {sendMessage.isPending && (
              <div className="flex justify-start">
                <div className="bg-gray-100 p-3 rounded-lg">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Suggested Products */}
          {sendMessage.data?.suggested_products &&
            sendMessage.data.suggested_products.length > 0 && (
              <div className="px-4 pb-2">
                <p className="text-xs text-gray-500 mb-2">Sản phẩm gợi ý:</p>
                <div className="flex space-x-2 overflow-x-auto pb-2">
                  {sendMessage.data.suggested_products.map((p) => (
                    <Link
                      key={p.product_id}
                      href={`/products/${p.product_id}`}
                      className="flex-shrink-0 w-28 p-2 bg-gray-50 rounded-lg hover:bg-gray-100"
                    >
                      <div className="w-full h-16 bg-gray-200 rounded mb-1" />
                      <p className="text-xs font-medium truncate">{p.name}</p>
                      <p className="text-xs text-blue-600">{formatPrice(p.price)}</p>
                    </Link>
                  ))}
                </div>
              </div>
            )}

          {/* Input */}
          <form onSubmit={handleSubmit} className="p-4 border-t">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Nhập tin nhắn..."
                className="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={sendMessage.isPending}
              />
              <button
                type="submit"
                disabled={sendMessage.isPending || !input.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}
