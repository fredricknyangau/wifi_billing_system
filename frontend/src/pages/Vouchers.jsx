import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Plus, Printer, RefreshCw } from 'lucide-react';
import Button from '../components/ui/Button';
import Table, { TableRow, TableCell } from '../components/ui/Table';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Input from '../components/ui/Input';

const Vouchers = () => {
    const [vouchers, setVouchers] = useState([]);
    const [plans, setPlans] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [generateData, setGenerateData] = useState({ plan_id: '', count: 1 });
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetchVouchers();
        fetchPlans();
    }, []);

    const fetchVouchers = async () => {
        setIsLoading(true);
        try {
            const response = await api.get('/billing/vouchers/');
            setVouchers(response.data);
        } catch (error) {
            console.error('Failed to fetch vouchers', error);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchPlans = async () => {
        try {
            const response = await api.get('/billing/plans/');
            setPlans(response.data);
        } catch (error) {
            console.error('Failed to fetch plans', error);
        }
    };

    const handleGenerate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/billing/vouchers/generate/', generateData);
            setShowModal(false);
            setGenerateData({ plan_id: '', count: 1 });
            fetchVouchers();
        } catch (error) {
            console.error('Failed to generate vouchers', error);
        }
    };

    const getStatusVariant = (status) => {
        switch (status) {
            case 'ACTIVE': return 'success';
            case 'USED': return 'default';
            case 'EXPIRED': return 'danger';
            default: return 'default';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Vouchers</h1>
                <div className="flex space-x-3">
                    <Button variant="secondary" onClick={fetchVouchers}>
                        <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                        Refresh
                    </Button>
                    <Button onClick={() => setShowModal(true)}>
                        <Plus className="w-4 h-4 mr-2" />
                        Generate
                    </Button>
                </div>
            </div>

            <Card>
                <Table headers={['Code', 'Plan', 'Status', 'Created At', 'Actions']}>
                    {vouchers.map((voucher) => (
                        <TableRow key={voucher.id}>
                            <TableCell className="font-mono font-bold text-gray-900">{voucher.code}</TableCell>
                            <TableCell>{voucher.plan_name}</TableCell>
                            <TableCell>
                                <Badge variant={getStatusVariant(voucher.status)}>
                                    {voucher.status}
                                </Badge>
                            </TableCell>
                            <TableCell>{new Date(voucher.created_at).toLocaleDateString()}</TableCell>
                            <TableCell>
                                <button className="text-gray-600 hover:text-gray-900" title="Print">
                                    <Printer className="w-4 h-4" />
                                </button>
                            </TableCell>
                        </TableRow>
                    ))}
                    {vouchers.length === 0 && (
                        <TableRow>
                            <TableCell className="text-center py-8" colSpan={5}>
                                No vouchers found. Generate some to get started.
                            </TableCell>
                        </TableRow>
                    )}
                </Table>
            </Card>

            {showModal && (
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
                        <h2 className="text-xl font-bold mb-4 text-gray-900">Generate Vouchers</h2>
                        <form onSubmit={handleGenerate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Select Plan</label>
                                <select
                                    className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                    value={generateData.plan_id}
                                    onChange={(e) => setGenerateData({ ...generateData, plan_id: e.target.value })}
                                    required
                                >
                                    <option value="">Select a plan...</option>
                                    {plans.map(plan => (
                                        <option key={plan.id} value={plan.id}>{plan.name} - {plan.price} KES</option>
                                    ))}
                                </select>
                            </div>

                            <Input
                                label="Quantity"
                                type="number"
                                value={generateData.count}
                                onChange={(e) => setGenerateData({ ...generateData, count: e.target.value })}
                                min="1"
                                max="100"
                                required
                            />

                            <div className="mt-6 flex justify-end space-x-3 pt-4 border-t">
                                <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>
                                    Cancel
                                </Button>
                                <Button type="submit" variant="primary"> // Changed to primary (green in original, but sticking to theme)
                                    Generate
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Vouchers;
