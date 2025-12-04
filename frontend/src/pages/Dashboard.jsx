import React, { useEffect, useState } from 'react';
import { Users, Wifi, CreditCard, TrendingUp } from 'lucide-react';
import Card from '../components/ui/Card';
import api from '../api/axios';
import UsageGauge from '../components/UsageGauge';
import CostPredictor from '../components/CostPredictor';
import NetworkHealth from '../components/NetworkHealth';

const Dashboard = () => {
    const [stats, setStats] = useState({
        total_users: 0,
        total_revenue: 0,
        total_data_usage: 0,
        active_vouchers: 0
    });

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await api.get('/reports/dashboard-stats/');
            setStats(response.data);
        } catch (error) {
            console.error('Failed to fetch dashboard stats', error);
        }
    };

    const displayStats = [
        { name: 'Total Revenue', value: `${stats.total_revenue} KES`, change: '+12%', changeType: 'positive', icon: CreditCard },
        { name: 'Active Vouchers', value: stats.active_vouchers, change: '+4%', changeType: 'positive', icon: Wifi },
        { name: 'Total Customers', value: stats.total_users, change: '+2.3%', changeType: 'positive', icon: Users },
        { name: 'Total Data Usage', value: `${(stats.total_data_usage / (1024 * 1024 * 1024)).toFixed(2)} GB`, change: '+10%', changeType: 'positive', icon: TrendingUp },
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
            <div className="md:flex md:items-center md:justify-between">
                <div className="flex-1 min-w-0">
                    <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                        Dashboard
                    </h2>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                {displayStats.map((item) => {
                    const Icon = item.icon;
                    return (
                        <Card key={item.name} className="px-4 py-5 sm:p-6 hover:shadow-lg transition-shadow duration-300 ease-in-out border border-gray-100">
                            <div className="flex items-center">
                                <div className="flex-shrink-0 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg p-3 shadow-md">
                                    <Icon className="h-6 w-6 text-white" aria-hidden="true" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dt className="text-sm font-bold text-gray-500 truncate uppercase tracking-wider">{item.name}</dt>
                                    <dd className="flex items-baseline mt-1">
                                        <div className="text-3xl font-extrabold text-gray-900">{item.value}</div>
                                    </dd>
                                </div>
                            </div>
                        </Card>
                    );
                })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1">
                    <UsageGauge 
                        speed={25} 
                        forecast={{
                            current_usage_gb: 45.5,
                            plan_limit_gb: 100,
                            projected_usage_gb: 90
                        }}
                    />
                </div>
                <div className="lg:col-span-1">
                    <CostPredictor 
                        costData={{
                            current_bill_estimate: 1500,
                            savings: 200
                        }}
                    />
                </div>
                <div className="lg:col-span-1">
                    <NetworkHealth 
                        networkData={{
                            status: 'GOOD',
                            region: 'Nairobi West',
                            avg_speed: 45,
                            uptime: 99.9
                        }}
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <Card title="Recent Activity" className="h-full hover:shadow-md transition-shadow duration-300">
                    <div className="text-center py-12 text-gray-500 flex flex-col items-center justify-center h-64 border-2 border-dashed border-gray-200 rounded-lg bg-gray-50">
                        <TrendingUp className="h-12 w-12 text-gray-300 mb-3" />
                        <p className="text-lg font-medium">No recent activity</p>
                        <p className="text-sm">Transactions will appear here once they occur.</p>
                    </div>
                </Card>
                <Card title="System Status" className="h-full hover:shadow-md transition-shadow duration-300">
                    <div className="space-y-6">
                        <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="flex items-center">
                                <div className="h-2.5 w-2.5 rounded-full bg-green-500 mr-3 animate-pulse"></div>
                                <span className="text-gray-700 font-medium">RADIUS Server</span>
                            </div>
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Operational
                            </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="flex items-center">
                                <div className="h-2.5 w-2.5 rounded-full bg-green-500 mr-3 animate-pulse"></div>
                                <span className="text-gray-700 font-medium">Database</span>
                            </div>
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                Operational
                            </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
                            <div className="flex items-center">
                                <div className="h-2.5 w-2.5 rounded-full bg-yellow-500 mr-3"></div>
                                <span className="text-gray-700 font-medium">M-Pesa Gateway</span>
                            </div>
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                Degraded
                            </span>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Dashboard;
