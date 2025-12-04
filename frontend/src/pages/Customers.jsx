import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Table, { TableRow, TableCell } from '../components/ui/Table';
import Card from '../components/ui/Card';
import { Search } from 'lucide-react';
import Input from '../components/ui/Input';

const Customers = () => {
    const [customers, setCustomers] = useState([]);

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await api.get('/customers/');
            setCustomers(response.data);
        } catch (error) {
            console.error('Failed to fetch customers', error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
                <div className="w-64">
                    <div className="relative rounded-md shadow-sm">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <Search className="h-4 w-4 text-gray-400" />
                        </div>
                        <input
                            type="text"
                            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
                            placeholder="Search customers..."
                        />
                    </div>
                </div>
            </div>

            <Card>
                <Table headers={['Username', 'Email', 'Balance', 'Joined', 'Status']}>
                    {customers.map((customer) => (
                        <TableRow key={customer.id}>
                            <TableCell className="font-medium text-gray-900">{customer.user.username}</TableCell>
                            <TableCell>{customer.user.email || '-'}</TableCell>
                            <TableCell className="font-bold text-gray-900">{customer.balance} KES</TableCell>
                            <TableCell>{new Date(customer.created_at).toLocaleDateString()}</TableCell>
                            <TableCell>
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                    Active
                                </span>
                            </TableCell>
                        </TableRow>
                    ))}
                    {customers.length === 0 && (
                        <TableRow>
                            <TableCell className="text-center py-8" colSpan={5}>
                                No customers found.
                            </TableCell>
                        </TableRow>
                    )}
                </Table>
            </Card>
        </div>
    );
};

export default Customers;
