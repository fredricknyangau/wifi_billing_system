import React, { useState } from 'react';
import { Users, DollarSign, PieChart } from 'lucide-react';
import Card from '../components/ui/Card';

const SocialBilling = () => {
    const [groupName, setGroupName] = useState('Apartment 4B');
    const [members, setMembers] = useState([
        { id: 1, name: 'You', share: 1000, status: 'PAID' },
        { id: 2, name: 'John Doe', share: 1000, status: 'PENDING' },
        { id: 3, name: 'Jane Smith', share: 1000, status: 'PENDING' },
    ]);

    const totalBill = 3000;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
            <div className="md:flex md:items-center md:justify-between">
                <div className="flex-1 min-w-0">
                    <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                        Social Billing & Groups
                    </h2>
                </div>
                <div className="mt-4 flex md:mt-0 md:ml-4">
                    <button
                        type="button"
                        className="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Create New Group
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Group Overview */}
                <div className="lg:col-span-2 space-y-8">
                    <Card title={`Group: ${groupName}`}>
                        <div className="mt-4">
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-gray-500">Total Monthly Bill</span>
                                <span className="text-2xl font-bold text-gray-900">{totalBill} KES</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                                <div className="bg-indigo-600 h-2.5 rounded-full" style={{ width: '33%' }}></div>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-indigo-600 font-medium">1,000 KES Paid</span>
                                <span className="text-gray-500">2,000 KES Remaining</span>
                            </div>
                        </div>
                    </Card>

                    <Card title="Members & Shares">
                        <ul className="divide-y divide-gray-200">
                            {members.map((member) => (
                                <li key={member.id} className="py-4 flex items-center justify-between">
                                    <div className="flex items-center">
                                        <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                                            <span className="text-indigo-800 font-medium">{member.name.charAt(0)}</span>
                                        </div>
                                        <div className="ml-3">
                                            <p className="text-sm font-medium text-gray-900">{member.name}</p>
                                            <p className="text-sm text-gray-500">Share: {member.share} KES</p>
                                        </div>
                                    </div>
                                    <div>
                                        {member.status === 'PAID' ? (
                                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                Paid
                                            </span>
                                        ) : (
                                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                                Pending
                                            </span>
                                        )}
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </Card>
                </div>

                {/* Actions */}
                <div className="space-y-8">
                    <Card title="Your Share">
                        <div className="text-center py-6">
                            <p className="text-sm text-gray-500 mb-1">Amount Due</p>
                            <p className="text-3xl font-bold text-gray-900 mb-6">0 KES</p>
                            <button
                                disabled
                                className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-500 cursor-not-allowed opacity-75"
                            >
                                Paid via M-Pesa
                            </button>
                            <p className="mt-4 text-xs text-gray-400">Next payment due: Jan 1, 2026</p>
                        </div>
                    </Card>

                    <Card title="Invite Members">
                        <div className="mt-2">
                            <p className="text-sm text-gray-500 mb-4">
                                Share the cost with roommates or neighbors.
                            </p>
                            <div className="flex space-x-2">
                                <input
                                    type="email"
                                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                    placeholder="Enter email address"
                                />
                                <button
                                    type="button"
                                    className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                >
                                    Invite
                                </button>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default SocialBilling;
