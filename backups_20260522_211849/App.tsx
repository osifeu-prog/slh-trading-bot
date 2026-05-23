import { useWebSocket } from './hooks/useWebSocket';
import { Activity, TrendingUp, DollarSign } from 'lucide-react';

function App() {
  const { data, isConnected } = useWebSocket();

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">SLH Trading Bot</h1>
          <div className={px-4 py-1 rounded-full text-sm flex items-center gap-2 \}>
            {isConnected ? '● Live' : '○ Disconnected'}
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-900 p-6 rounded-xl">
            <DollarSign className="w-8 h-8 text-emerald-400 mb-4" />
            <p className="text-gray-400">Last Price</p>
            <p className="text-4xl font-bold mt-2">
              {data?.last_trade?.price ? \}{data.last_trade.price} : '—'}
            </p>
            <p className="text-sm text-gray-500">{data?.last_trade?.symbol}</p>
          </div>

          <div className="bg-gray-900 p-6 rounded-xl">
            <TrendingUp className="w-8 h-8 text-blue-400 mb-4" />
            <p className="text-gray-400">PnL</p>
            <p className="text-4xl font-bold mt-2">
              {data?.pnl !== null ? \}{data.pnl.toFixed(2)} : '—'}
            </p>
          </div>

          <div className="bg-gray-900 p-6 rounded-xl">
            <Activity className="w-8 h-8 text-purple-400 mb-4" />
            <p className="text-gray-400">Status</p>
            <p className="text-3xl font-bold mt-2 text-emerald-400">
              {data?.status || 'LIVE'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-gray-900 p-6 rounded-xl">
            <h2 className="text-xl mb-4">Open Positions</h2>
            {data?.positions?.length > 0 ? (
              <pre>{JSON.stringify(data.positions, null, 2)}</pre>
            ) : (
              <p className="text-gray-500">No open positions</p>
            )}
          </div>

          <div className="bg-gray-900 p-6 rounded-xl">
            <h2 className="text-xl mb-4">Recent Activity</h2>
            <p className="text-gray-500">Last update: {data?.timestamp}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
