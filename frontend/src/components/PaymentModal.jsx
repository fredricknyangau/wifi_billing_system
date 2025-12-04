import React, { useState } from 'react';
import Button from './ui/Button';
import Input from './ui/Input';
import api from '../api/axios';

const PaymentModal = ({ plan, onClose, onSuccess }) => {
    const [phoneNumber, setPhoneNumber] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handlePayment = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            // In a real app, this would trigger the STK push
            await api.post('/billing/mpesa/pay', {
                phone_number: phoneNumber,
                amount: plan.price
            });
            onSuccess();
        } catch (err) {
            setError('Failed to initiate payment. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
                <h2 className="text-xl font-bold mb-4 text-gray-900">Purchase {plan.name}</h2>
                <p className="text-gray-600 mb-6">
                    You are about to purchase the <span className="font-semibold">{plan.name}</span> plan for <span className="font-bold text-indigo-600">{plan.price} KES</span>.
                </p>

                {error && (
                    <div className="bg-red-50 text-red-700 p-3 rounded mb-4 text-sm">
                        {error}
                    </div>
                )}

                <form onSubmit={handlePayment} className="space-y-4">
                    <Input
                        label="M-Pesa Phone Number"
                        placeholder="2547..."
                        value={phoneNumber}
                        onChange={(e) => {
                            const value = e.target.value;
                            setPhoneNumber(value);
                            if (value && !value.startsWith('254')) {
                                setError('Phone number must start with 254');
                            } else {
                                setError('');
                            }
                        }}
                        required
                        pattern="^254\d{9}$" // Enforce pattern: starts with 254 followed by 9 digits
                        title="Phone number must start with '254' (e.g., 2547XXXXXXXX)"
                    />

                    <div className="mt-6 flex justify-end space-x-3 pt-4 ">
                        <Button variant="secondary" type="button" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading ? 'Processing...' : 'Pay with M-Pesa'}
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default PaymentModal;
