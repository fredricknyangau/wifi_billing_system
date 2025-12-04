import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Table, { TableRow, TableCell } from '../components/ui/Table';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';

const Transactions = () => {
    const [transactions, setTransactions] = useState([]);
    const [phoneNumber, setPhoneNumber] = useState('');
    const [searched, setSearched] = useState(false);

    const fetchTransactions = async (e) => {
        e.preventDefault();
        if (!phoneNumber) return;

        try {
            const response = await api.get(`/billing/transactions/?phone_number=${phoneNumber}`);
            setTransactions(response.data);
            setSearched(true);
        } catch (error) {
            console.error('Failed to fetch transactions', error);
            setTransactions([]);
            setSearched(true);
        }
    };

    const getStatusVariant = (status) => {
        return status === 'Completed' ? 'success' : 'warning';
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Transactions</h1>

            <Card>
                <form onSubmit={fetchTransactions} className="mb-6">
                    <label htmlFor="trans-phone-search" className="block text-sm font-medium text-gray-700 mb-2">
                        Enter Phone Number to View Transactions
                    </label>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            id="trans-phone-search"
                            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                            placeholder="e.g. 254712345678"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                        />
                        <button
                            type="submit"
                            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Search
                        </button>
                    </div>
                </form>

                {searched && (
                    <Table headers={['Receipt', 'Phone', 'Amount', 'Status', 'Date']}>
                        {transactions.map((transaction) => (
                            <TableRow key={transaction.id}>
                                <TableCell className="font-mono text-gray-900">{transaction.receipt_number}</TableCell>
                                <TableCell>{transaction.phone_number}</TableCell>
                                <TableCell className="font-bold text-gray-900">{transaction.amount} KES</TableCell>
                                <TableCell>
                                    <Badge variant={getStatusVariant(transaction.status)}>
                                        {transaction.status}
                                    </Badge>
                                </TableCell>
                                <TableCell>{new Date(transaction.transaction_date).toLocaleString()}</TableCell>
                            </TableRow>
                        ))}
                        {transactions.length === 0 && (
                            <TableRow>
                                <TableCell className="text-center py-8" colSpan={5}>
                                    No transactions found for this number.
                                </TableCell>
                            </TableRow>
                        )}
                    </Table>
                )}
            </Card>
        </div>
    );
};

export default Transactions;
