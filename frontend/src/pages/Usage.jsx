import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import Table, { TableRow, TableCell } from '../components/ui/Table';
import Card from '../components/ui/Card';

const Usage = () => {
    const [usageData, setUsageData] = useState([]);
    const [phoneNumber, setPhoneNumber] = useState('');
    const [searched, setSearched] = useState(false);

    const fetchUsage = async (e) => {
        e.preventDefault();
        if (!phoneNumber) return;
        
        try {
            const response = await api.get(`/usage/?phone_number=${phoneNumber}`);
            setUsageData(response.data);
            setSearched(true);
        } catch (error) {
            console.error('Failed to fetch usage data', error);
            setUsageData([]);
            setSearched(true);
        }
    };

    const formatBytes = (bytes, decimals = 2) => {
        if (!+bytes) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Data Usage</h1>
            </div>

            <Card>
                <form onSubmit={fetchUsage} className="mb-6">
                    <label htmlFor="phone-search" className="block text-sm font-medium text-gray-700 mb-2">
                        Enter Phone Number to View Usage
                    </label>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            id="phone-search"
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
                    <Table headers={['User', 'Session Start', 'Session End', 'Upload', 'Download']}>
                        {usageData.map((usage) => (
                            <TableRow key={usage.id}>
                                <TableCell className="font-medium text-gray-900">{usage.user}</TableCell>
                                <TableCell>{new Date(usage.session_start).toLocaleString()}</TableCell>
                                <TableCell>{usage.session_end ? new Date(usage.session_end).toLocaleString() : 'Active'}</TableCell>
                                <TableCell>{formatBytes(usage.upload_bytes)}</TableCell>
                                <TableCell>{formatBytes(usage.download_bytes)}</TableCell>
                            </TableRow>
                        ))}
                        {usageData.length === 0 && (
                            <TableRow>
                                <TableCell className="text-center py-8" colSpan={5}>
                                    No usage data found for this number.
                                </TableCell>
                            </TableRow>
                        )}
                    </Table>
                )}
            </Card>
        </div>
    );
};

export default Usage;
