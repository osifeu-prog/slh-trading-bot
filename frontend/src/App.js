import React from 'react';
import { useWebSocket } from './hooks/useWebSocket';

function App() {
  const data = useWebSocket('ws://localhost:8080/ws/price');

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>📈 SLH Trading Bot Dashboard</h1>
      {data ? (
        <div>
          <p><strong>Symbol:</strong> {data.symbol}</p>
          <p><strong>Price:</strong> ${data.price.toLocaleString()}</p>
          <p><strong>SMA9:</strong> {data.sma_short?.toFixed(2)}</p>
          <p><strong>SMA21:</strong> {data.sma_long?.toFixed(2)}</p>
          <p><strong>RSI:</strong> {data.rsi?.toFixed(1)}</p>
          <p><strong>Position:</strong> {data.in_position ? '🔴 Long' : '⚪ Flat'}</p>
          <p><small>Last update: {new Date(data.timestamp).toLocaleTimeString()}</small></p>
        </div>
      ) : (
        <p>⏳ Waiting for WebSocket data...</p>
      )}
    </div>
  );
}

export default App;
