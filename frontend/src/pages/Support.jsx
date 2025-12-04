import React, { useState } from 'react';
import { MessageSquare, AlertCircle, CheckCircle } from 'lucide-react';
import Card from '../components/ui/Card';

const Support = () => {
    const [tickets, setTickets] = useState([
        { id: 101, subject: 'Slow Internet', status: 'RESOLVED', priority: 'HIGH', sentiment: 'NEGATIVE', date: '2025-12-01' },
        { id: 102, subject: 'Billing Inquiry', status: 'OPEN', priority: 'MEDIUM', sentiment: 'NEUTRAL', date: '2025-12-03' },
    ]);

    const [newTicket, setNewTicket] = useState({ subject: '', description: '' });

    const handleSubmit = (e) => {
        e.preventDefault();
        // Mock submission
        const ticket = {
            id: tickets.length + 101,
            subject: newTicket.subject,
            status: 'OPEN',
            priority: 'ANALYZING...', // AI would set this
            sentiment: 'ANALYZING...', // AI would set this
            date: new Date().toISOString().split('T')[0]
        };
        setTickets([ticket, ...tickets]);
        setNewTicket({ subject: '', description: '' });
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
            <div className="md:flex md:items-center md:justify-between">
                <div className="flex-1 min-w-0">
                    <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                        Intelligent Support
                    </h2>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* New Ticket Form */}
                <Card title="Create New Ticket">
                    <form onSubmit={handleSubmit} className="space-y-6 mt-4">
                        <div>
                            <label htmlFor="subject" className="block text-sm font-medium text-gray-700">
                                Subject
                            </label>
                            <div className="mt-1">
                                <input
                                    type="text"
                                    name="subject"
                                    id="subject"
                                    required
                                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                    value={newTicket.subject}
                                    onChange={(e) => setNewTicket({ ...newTicket, subject: e.target.value })}
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                                Description
                            </label>
                            <div className="mt-1">
                                <textarea
                                    id="description"
                                    name="description"
                                    rows={4}
                                    required
                                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                    value={newTicket.description}
                                    onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                                />
                            </div>
                            <p className="mt-2 text-sm text-gray-500">
                                Our AI will analyze your request and prioritize it automatically.
                            </p>
                        </div>

                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Submit Ticket
                        </button>
                    </form>
                </Card>

                {/* Recent Tickets */}
                <Card title="Recent Tickets">
                    <div className="flow-root mt-4">
                        <ul className="-my-5 divide-y divide-gray-200">
                            {tickets.map((ticket) => (
                                <li key={ticket.id} className="py-4">
                                    <div className="flex items-center space-x-4">
                                        <div className="flex-shrink-0">
                                            {ticket.status === 'RESOLVED' ? (
                                                <CheckCircle className="h-6 w-6 text-green-500" />
                                            ) : (
                                                <AlertCircle className="h-6 w-6 text-yellow-500" />
                                            )}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm font-medium text-gray-900 truncate">
                                                {ticket.subject}
                                            </p>
                                            <p className="text-sm text-gray-500 truncate">
                                                ID: #{ticket.id} • {ticket.date}
                                            </p>
                                        </div>
                                        <div className="inline-flex flex-col items-end space-y-1">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                ticket.status === 'RESOLVED' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                                {ticket.status}
                                            </span>
                                            {ticket.priority && (
                                                 <span className="text-xs text-gray-400">
                                                    Priority: {ticket.priority}
                                                 </span>
                                            )}
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Support;
