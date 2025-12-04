import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Plus, Trash, Edit2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Table, { TableRow, TableCell } from '../components/ui/Table';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';

const Plans = () => {
    const [plans, setPlans] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [newPlan, setNewPlan] = useState({ name: '', price: '', duration_minutes: '', speed_limit: '' });

    useEffect(() => {
        fetchPlans();
    }, []);

    const fetchPlans = async () => {
        try {
            const response = await api.get('/billing/plans/');
            setPlans(response.data);
        } catch (error) {
            console.error('Failed to fetch plans', error);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/billing/plans/', newPlan);
            setShowModal(false);
            setNewPlan({ name: '', price: '', duration_minutes: '', speed_limit: '' });
            fetchPlans();
        } catch (error) {
            console.error('Failed to create plan', error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Pricing Plans</h1>
                <Button onClick={() => setShowModal(true)}>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Plan
                </Button>
            </div>

            <Card>
                <Table headers={['Name', 'Price', 'Duration', 'Speed Limit', 'Actions']}>
                    {plans.map((plan) => (
                        <TableRow key={plan.id}>
                            <TableCell className="font-medium text-gray-900">{plan.name}</TableCell>
                            <TableCell>{plan.price} KES</TableCell>
                            <TableCell>{plan.duration_minutes} Mins</TableCell>
                            <TableCell>
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                    {plan.speed_limit}
                                </span>
                            </TableCell>
                            <TableCell>
                                <div className="flex space-x-3">
                                    <button className="text-indigo-600 hover:text-indigo-900">
                                        <Edit2 className="w-4 h-4" />
                                    </button>
                                    <button className="text-red-600 hover:text-red-900">
                                        <Trash className="w-4 h-4" />
                                    </button>
                                </div>
                            </TableCell>
                        </TableRow>
                    ))}
                    {plans.length === 0 && (
                        <TableRow>
                            <TableCell className="text-center py-8" colSpan={5}>
                                No plans found. Create one to get started.
                            </TableCell>
                        </TableRow>
                    )}
                </Table>
            </Card>

            {showModal && (
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
                        <h2 className="text-xl font-bold mb-4 text-gray-900">Create New Plan</h2>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <Input
                                label="Plan Name"
                                value={newPlan.name}
                                onChange={(e) => setNewPlan({ ...newPlan, name: e.target.value })}
                                required
                            />
                            <Input
                                label="Price (KES)"
                                type="number"
                                value={newPlan.price}
                                onChange={(e) => setNewPlan({ ...newPlan, price: e.target.value })}
                                required
                            />
                            <Input
                                label="Duration (Minutes)"
                                type="number"
                                value={newPlan.duration_minutes}
                                onChange={(e) => setNewPlan({ ...newPlan, duration_minutes: e.target.value })}
                                required
                            />
                            <Input
                                label="Speed Limit (e.g. 2M/5M)"
                                value={newPlan.speed_limit}
                                onChange={(e) => setNewPlan({ ...newPlan, speed_limit: e.target.value })}
                                required
                            />

                            <div className="mt-6 flex justify-end space-x-3 pt-4 border-t">
                                <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>
                                    Cancel
                                </Button>
                                <Button type="submit">
                                    Create Plan
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Plans;
