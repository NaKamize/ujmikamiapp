import { useEffect, useRef, useState, type FormEvent } from 'react';
import Markdown from 'markdown-to-jsx';
import './ChatWidget.css';

const AI_SERVICE_URL = process.env.REACT_APP_AI_SERVICE_URL;
const REQUEST_TIMEOUT_MS = 20000;
const OFFLINE_MESSAGE =
  'Notice: The local AI microservice is currently offline. To see this LangGraph agent run locally, clone the repository, run `docker compose up`, and refresh this page.';

type ChatRole = 'user' | 'assistant' | 'system';

interface ChatMessage {
  id: number;
  role: ChatRole;
  content: string;
}

let nextMessageId = 0;

function createMessage(role: ChatRole, content: string): ChatMessage {
  nextMessageId += 1;
  return { id: nextMessageId, role, content };
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isWaiting, setIsWaiting] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  const feedRef = useRef<HTMLDivElement>(null);
  const stickToBottomRef = useRef(true);

  useEffect(() => {
    const feed = feedRef.current;
    if (feed && stickToBottomRef.current) {
      feed.scrollTop = feed.scrollHeight;
    }
  }, [messages, isWaiting]);

  function handleFeedScroll() {
    const feed = feedRef.current;
    if (!feed) return;
    const distanceFromBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight;
    stickToBottomRef.current = distanceFromBottom < 48;
  }

  async function sendMessage(query: string) {
    setMessages((prev) => [...prev, createMessage('user', query)]);

    if (!AI_SERVICE_URL) {
      setMessages((prev) => [...prev, createMessage('system', OFFLINE_MESSAGE)]);
      return;
    }

    stickToBottomRef.current = true;
    setIsWaiting(true);

    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
      const response = await fetch(`${AI_SERVICE_URL}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
        signal: controller.signal,
      });

      if (!response.ok || !response.body) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessageId: number | null = null;

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        if (!chunk) continue;

        if (assistantMessageId === null) {
          setIsWaiting(false);
          setIsStreaming(true);
          const message = createMessage('assistant', chunk);
          assistantMessageId = message.id;
          setMessages((prev) => [...prev, message]);
        } else {
          const id = assistantMessageId;
          setMessages((prev) =>
            prev.map((m) => (m.id === id ? { ...m, content: m.content + chunk } : m))
          );
        }
      }
    } catch {
      setMessages((prev) => [...prev, createMessage('system', OFFLINE_MESSAGE)]);
    } finally {
      window.clearTimeout(timeoutId);
      setIsWaiting(false);
      setIsStreaming(false);
    }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const query = input.trim();
    if (!query || isWaiting || isStreaming) return;
    setInput('');
    sendMessage(query);
  }

  const busy = isWaiting || isStreaming;

  return (
    <div className="chat-widget">
      <div className={`chat-widget__panel ${isOpen ? 'chat-widget__panel--open' : ''}`}>
        <div className="chat-widget__header">
          <span>Ask about Jozef&apos;s work</span>
          <button
            type="button"
            className="chat-widget__close"
            aria-label="Close chat"
            onClick={() => setIsOpen(false)}
          >
            ×
          </button>
        </div>

        <div className="chat-widget__feed" ref={feedRef} onScroll={handleFeedScroll}>
          {messages.length === 0 && (
            <div className="chat-widget__message chat-widget__message--system">
              Ask me anything about Jozef&apos;s projects, publications, or background.
            </div>
          )}
          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-widget__message chat-widget__message--${message.role}`}
            >
              <Markdown>{message.content}</Markdown>
            </div>
          ))}
          {isWaiting && (
            <div className="chat-widget__typing" aria-label="Agent is thinking">
              <span />
              <span />
              <span />
            </div>
          )}
        </div>

        <form className="chat-widget__composer" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask a question..."
            disabled={busy}
          />
          <button type="submit" disabled={busy || input.trim().length === 0}>
            Send
          </button>
        </form>
      </div>

      <button
        type="button"
        className="chat-widget__fab"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        onClick={() => setIsOpen((prev) => !prev)}
      >
        {isOpen ? '×' : '💬'}
      </button>
    </div>
  );
}
