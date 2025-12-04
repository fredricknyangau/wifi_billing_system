import React from 'react';

const NetworkHealth = ({ networkData }) => {
  const getStatusColor = (status) => {
    switch(status) {
      case 'GOOD': return 'text-green-600';
      case 'CONGESTED': return 'text-yellow-600';
      case 'OUTAGE': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-2">Network Health</h3>
      <div className="flex items-center">
        <div className={`text-xl font-bold ${getStatusColor(networkData.status)}`}>
          {networkData.status}
        </div>
        <span className="mx-2 text-gray-300">|</span>
        <div className="text-gray-600">{networkData.region}</div>
      </div>
      <div className="mt-2 text-sm text-gray-500">
        <div>Avg Speed: {networkData.avg_speed} Mbps</div>
        <div>Uptime: {networkData.uptime}%</div>
      </div>
    </div>
  );
};

export default NetworkHealth;
