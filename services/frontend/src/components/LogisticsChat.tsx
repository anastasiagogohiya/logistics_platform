import React, { useState, useEffect, useRef } from 'react';
import './LogisticsChat.css';

// ========== ТИПЫ ==========
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: number;
}

interface Offer {
  option_number: number;
  tariff_id: number;
  carrier_name: string;
  price: number;
  delivery_days: number;
  is_express?: boolean;
}

interface ChatResponse {
  parsed: Record<string, any>;
  offers: Offer[];
  message: string;
  need_clarification: boolean;
}

interface User {
  username: string;
}

const API_URL = 'http://localhost:8000';

const LogisticsChat: React.FC = () => {
  // --- Авторизация ---
  const [user, setUser] = useState<User | null>(null);
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [registerUsername, setRegisterUsername] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [authError, setAuthError] = useState('');

  // --- Чат ---
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '👋 Привет! Я твой транспортный помощник!\n\nНапиши, что нужно перевезти, или просто начни диалог.\n\n📝 Пример: "Перевези диван из Москвы в Питер, вес 50 кг, завтра"',
      sender: 'ai',
      timestamp: Date.now(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() =>
    `session_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`
  );

  // --- Состояния для кнопок ---
  const [offers, setOffers] = useState<Offer[]>([]);
  const [dialogState, setDialogState] = useState<'idle' | 'awaiting_choice' | 'awaiting_confirmation'>('idle');

  // --- Refs ---
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // --- Эффекты ---
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) textareaRef.current.focus();
  }, []);

  // Автоматическая высота textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [inputValue]);

  // Очистка таймера при размонтировании
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  // ========== ВХОД (ЛОГИН) ==========
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    try {
      const res = await fetch(`${API_URL}/api/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: loginUsername.trim(),
          password: loginPassword.trim(),
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Неверный логин или пароль');
      }
      const data = await res.json();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      setUser({ username: loginUsername.trim() });
      setLoginUsername('');
      setLoginPassword('');
    } catch (error: any) {
      setAuthError(error.message);
    }
  };

  // ========== РЕГИСТРАЦИЯ ==========
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    try {
      const regRes = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: registerUsername.trim(),
          password: registerPassword.trim(),
        }),
      });
      if (!regRes.ok) {
        const err = await regRes.json();
        throw new Error(err.detail || 'Ошибка регистрации');
      }
      // После регистрации – логин
      const loginRes = await fetch(`${API_URL}/api/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: registerUsername.trim(),
          password: registerPassword.trim(),
        }),
      });
      if (!loginRes.ok) {
        throw new Error('Не удалось войти после регистрации');
      }
      const data = await loginRes.json();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      setUser({ username: registerUsername.trim() });
      setRegisterUsername('');
      setRegisterPassword('');
    } catch (error: any) {
      setAuthError(error.message);
    }
  };

  // ========== ВЫХОД ==========
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setMessages([
      {
        id: '1',
        text: '👋 Привет! Я твой логистический помощник!\n\nНапиши, что нужно перевезти, или просто начни диалог.\n📝 Пример: "Перевези диван из Москвы в Казань, вес 50 кг, 20.08.2026"',
        sender: 'ai',
        timestamp: Date.now(),
      },
    ]);
    setDialogState('idle');
    setOffers([]);
  };

  // ========== ОТПРАВКА ЗАПРОСА В БЭКЕНД ==========
  const sendToBackend = async (text: string): Promise<ChatResponse> => {
    const token = localStorage.getItem('access_token');
    const headers: HeadersInit = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_URL}/api/chat/process`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        text: text,
        session_id: sessionId,
      }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    return await response.json();
  };

  // ========== ОБЩАЯ ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ ==========
  const sendMessageWithText = async (text: string) => {
    if (!text.trim() || isLoading) return;
    const userText = text.trim();
    setMessages((prev) => [
      ...prev,
      { id: Date.now().toString(), text: userText, sender: 'user', timestamp: Date.now() },
    ]);
    setIsLoading(true);

    try {
      const data = await sendToBackend(userText);

      let botMessageText = data.message;

      if (data.offers && data.offers.length > 0 && !data.need_clarification) {
        const offersList = data.offers.map((o) =>
          `- ${o.carrier_name}: ${o.price} руб., срок ${o.delivery_days} дн.`
        ).join('\n');
        botMessageText += `\n\n${offersList}`;
      }

      setMessages((prev) => [
        ...prev,
        { id: `${Date.now()}-ai`, text: botMessageText, sender: 'ai', timestamp: Date.now() },
      ]);

      if (data.offers && data.offers.length > 0 && !data.need_clarification) {
        setOffers(data.offers);
        setDialogState('awaiting_choice');
        if (timerRef.current) clearTimeout(timerRef.current);
        timerRef.current = setTimeout(() => {
          setMessages((prev) => [
            ...prev,
            {
              id: `${Date.now()}-choose-hint`,
              text: '📌 Выберите номер варианта, чтобы оформить заказ.',
              sender: 'ai',
              timestamp: Date.now(),
            },
          ]);
        }, 400);
      } else if (data.need_clarification && data.message.includes('Подтвердите оформление заказа')) {
        setDialogState('awaiting_confirmation');
      } else {
        setDialogState('idle');
        setOffers([]);
      }
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `${Date.now()}-error`,
          text: `❌ Ошибка: ${error.message}`,
          sender: 'ai',
          timestamp: Date.now(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // ========== ОБРАБОТЧИКИ ДЛЯ КНОПОК ==========
  const handleChoice = (optionNumber: number) => {
    sendMessageWithText(optionNumber.toString());
  };

  const handleConfirmation = (answer: 'да' | 'нет') => {
    sendMessageWithText(answer);
  };

  // ========== ОБРАБОТЧИК ПОЛЯ ВВОДА ==========
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    setDialogState('idle');
    setOffers([]);
    await sendMessageWithText(inputValue);
    setInputValue('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // ========== ЕСЛИ НЕ АВТОРИЗОВАН ==========
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-chat-light">
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 w-full max-w-md border border-white/50">
          <div className="text-center mb-8">
            <div className="w-20 h-20 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center shadow-xl shadow-blue-500/50 mx-auto">
              <span className="text-4xl">🤖</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mt-4">Транспортный Помощник</h1>
            <p className="text-gray-500 mt-1">Войдите или зарегистрируйтесь</p>
          </div>
          {authError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-xl mb-4 text-sm">
              {authError}
            </div>
          )}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Логин</label>
              <input
                type="text"
                value={loginUsername}
                onChange={(e) => setLoginUsername(e.target.value)}
                placeholder="Введите логин"
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-transparent outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
              <input
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                placeholder="Введите пароль"
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-transparent outline-none transition"
              />
            </div>
            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              Войти
            </button>
          </form>
          <div className="my-4 flex items-center gap-4">
            <div className="flex-grow h-px bg-gray-300" />
            <span className="text-sm text-gray-400">или</span>
            <div className="flex-grow h-px bg-gray-300" />
          </div>
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Логин</label>
              <input
                type="text"
                value={registerUsername}
                onChange={(e) => setRegisterUsername(e.target.value)}
                placeholder="Придумайте логин"
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-400 focus:border-transparent outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
              <input
                type="password"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                placeholder="Придумайте пароль"
                className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-400 focus:border-transparent outline-none transition"
              />
            </div>
            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              Зарегистрироваться
            </button>
          </form>
        </div>
      </div>
    );
  }

  // ========== ОСНОВНОЙ ЧАТ (с фоновым изображением) ==========
  return (
    <div className="h-screen flex flex-col bg-chat-light">
      {/* Хедер — фиксирован сверху */}
      <header className="bg-white/80 backdrop-blur-md shadow-md px-6 py-3 flex-shrink-0 border-b border-gray-200/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center shadow">
              <span className="text-2xl">🤖</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">Транспортный Помощник</h1>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${dialogState !== 'idle' ? 'bg-green-500' : 'bg-blue-500'}`} />
                <p className="text-xs text-gray-600">
                  {dialogState !== 'idle' ? '⏳ Ожидание ответа' : '📝 Готов к запросу'}
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-gray-700 bg-white/50 px-3 py-1 rounded-full backdrop-blur-sm">
              👤 {user.username}
            </span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500/90 hover:bg-red-600 text-white rounded-full text-sm font-semibold shadow transition-colors backdrop-blur-sm"
            >
              Выйти
            </button>
          </div>
        </div>
      </header>

      {/* Основная область — занимает всё оставшееся пространство */}
      <main className="flex-1 overflow-hidden flex justify-center p-2">
        <div className="w-full h-full bg-white/80 backdrop-blur-md rounded-2xl shadow-xl flex flex-col overflow-hidden">
          {/* Окно сообщений — прокрутка только здесь */}
          <div
            ref={chatContainerRef}
            className="flex-1 p-6 space-y-4 overflow-y-auto"
            style={{ scrollbarWidth: 'thin' }}
          >
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[75%] px-5 py-3 rounded-2xl text-sm leading-relaxed shadow ${
                    msg.sender === 'user'
                      ? 'bg-blue-600/90 backdrop-blur-sm text-white rounded-br-none'
                      : 'bg-white/90 backdrop-blur-sm text-gray-800 rounded-bl-none'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-lg">{msg.sender === 'user' ? '👤' : '🤖'}</span>
                    <div>
                      <div className="whitespace-pre-line">{msg.text}</div>
                      <div className={`text-[10px] mt-1 ${msg.sender === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white/90 backdrop-blur-sm px-5 py-3 rounded-2xl rounded-bl-none shadow">
                  <div className="flex items-center gap-3">
                    <span className="text-xl animate-bounce">⚡</span>
                    <span className="text-gray-600">Обработка...</span>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Блок кнопок выбора / подтверждения и примеры */}
          <div className="px-4 pb-2 flex flex-col gap-2">
            {dialogState === 'awaiting_choice' && offers.length > 0 && (
              <div className="flex flex-wrap gap-2 justify-center">
                {offers.map((offer) => (
                  <button
                    key={offer.tariff_id}
                    onClick={() => handleChoice(offer.option_number)}
                    disabled={isLoading}
                    className="px-4 py-2 bg-blue-500/90 hover:bg-blue-600 text-white font-medium rounded-full shadow transition-all disabled:opacity-50 text-sm backdrop-blur-sm"
                  >
                    {offer.option_number}. {offer.carrier_name} – {offer.price} руб.
                  </button>
                ))}
              </div>
            )}

            {dialogState === 'awaiting_confirmation' && (
              <div className="flex gap-3 justify-center">
                <button
                  onClick={() => handleConfirmation('да')}
                  disabled={isLoading}
                  className="px-6 py-2 bg-green-500/90 hover:bg-green-600 text-white font-semibold rounded-full shadow transition-all disabled:opacity-50 backdrop-blur-sm"
                >
                  ✅ Да
                </button>
                <button
                  onClick={() => handleConfirmation('нет')}
                  disabled={isLoading}
                  className="px-6 py-2 bg-red-500/90 hover:bg-red-600 text-white font-semibold rounded-full shadow transition-all disabled:opacity-50 backdrop-blur-sm"
                >
                  ❌ Нет
                </button>
              </div>
            )}

            <div className="flex gap-2 flex-wrap justify-center">
              <button
                onClick={() => setInputValue('Перевези диван из Москвы в Казань, вес 50 кг, 20.07.2026')}
                className="text-xs bg-white/80 backdrop-blur-sm hover:bg-white text-blue-700 px-3 py-1 rounded-full border border-blue-200 transition-all"
              >
                📦 Пример 1
              </button>
              <button
                onClick={() => setInputValue('Нужно перевезти холодильник из Тбилиси в Москву, общий вес 100 кг, 01.09.2026, кол-во 2')}
                className="text-xs bg-white/80 backdrop-blur-sm hover:bg-white text-blue-700 px-3 py-1 rounded-full border border-blue-200 transition-all"
              >
                📦 Пример 2
              </button>
              <button
                onClick={() => setInputValue('Перевези из Москвы в Питер')}
                className="text-xs bg-white/80 backdrop-blur-sm hover:bg-white text-blue-700 px-3 py-1 rounded-full border border-blue-200 transition-all"
              >
                📦 Пример 3 (неполный)
              </button>
            </div>
          </div>

          {/* Поле ввода */}
          <div className="border-t border-gray-200/50 p-4 bg-white/80 backdrop-blur-sm rounded-b-2xl">
            <div className="flex items-end gap-3">
              <div className="relative flex-grow">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={
                    dialogState === 'awaiting_choice'
                      ? 'Выберите номер варианта (или напишите новый запрос)'
                      : dialogState === 'awaiting_confirmation'
                      ? 'Ответьте "да" или "нет" (или напишите новый запрос)'
                      : 'Введите сообщение...'
                  }
                  disabled={isLoading}
                  className="w-full p-3 pr-12 rounded-xl bg-white/90 backdrop-blur-sm border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent resize-none min-h-[44px] max-h-[150px] placeholder-gray-400 disabled:opacity-50 text-sm"
                  style={{ overflow: 'hidden' }}
                />
                <div className="absolute right-3 bottom-3 text-gray-400 text-[10px]">↵</div>
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="p-3 bg-gradient-to-r from-blue-500 to-purple-500 hover:scale-105 rounded-xl transition-all shadow-lg shadow-purple-400/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
              >
                <span className="text-xl">🚀</span>
              </button>
            </div>
            <div className="mt-2 text-center">
              <span className="inline-block text-xs text-gray-500 bg-white/80 backdrop-blur-sm px-3 py-1 rounded-full border border-gray-200">
                {dialogState === 'awaiting_choice'
                  ? '🔢 Выберите номер'
                  : dialogState === 'awaiting_confirmation'
                  ? '✅ Подтвердите заказ'
                  : '🧠 Отправьте запрос'}
              </span>
            </div>
          </div>
        </div>
      </main>

      {/* Футер */}
      <footer className="bg-white/70 backdrop-blur-sm border-t border-gray-200/50 py-1 px-3 flex-shrink-0 text-center text-xs text-gray-400">
        <span>🤖 ФРОНТЕНД · {API_URL} · {user.username}</span>
      </footer>
    </div>
  );
};

export default LogisticsChat;