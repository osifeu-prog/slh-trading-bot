import { useEffect, useState, useRef } from 'react';

const WS_URL = 'wss://giver-uncoated-sibling.ngrok-free.dev/ws'; // Change if Ngrok restarts

export function useWebSocket() {
  const [data, setData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('✅ WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (e) {
        console.error('WS Parse error', e);
      }
    };

    ws.onclose = () => {
      console.log('❌ WebSocket disconnected');
      setIsConnected(false);
    };

    ws.onerror = (error) => console.error('WS Error:', error);

    return () => ws.close();
  }, []);

  return { data, isConnected };
}
