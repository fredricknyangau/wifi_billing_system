import React from 'react';

const UsageGauge = ({ speed, forecast }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-2">Live Usage</h3>
      <div className="flex items-center justify-between">
        <div className="text-center">
          <div className="text-3xl font-bold text-blue-600">{speed} Mbps</div>
          <div className="text-sm text-gray-500">Current Speed</div>
        </div>
        <div className="w-px h-12 bg-gray-200"></div>
        <div className="text-center">
          <div className="text-xl font-semibold">{forecast.current_usage_gb} GB</div>
          <div className="text-sm text-gray-500">Used / {forecast.plan_limit_gb} GB</div>
        </div>
      </div>
      <div className="mt-4">
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div 
            className="bg-blue-600 h-2.5 rounded-full" 
            style={{ width: `${(forecast.current_usage_gb / forecast.plan_limit_gb) * 100}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-500 mt-1">Projected: {forecast.projected_usage_gb} GB</p>
      </div>
    </div>
  );
};

export default UsageGauge;
