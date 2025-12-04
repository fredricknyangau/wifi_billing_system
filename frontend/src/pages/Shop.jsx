import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import PaymentModal from '../components/PaymentModal';
import { Wifi, Check, Zap, Clock, Shield, CreditCard, Activity, UserPlus, MessageSquare, LayoutGrid, Menu, X } from 'lucide-react';
import Usage from './Usage';
import Transactions from './Transactions';
import SocialBilling from './SocialBilling';
import Support from './Support';

const Shop = () => {
    const [plans, setPlans] = useState([]);
    const [selectedPlan, setSelectedPlan] = useState(null);
    const [showSuccess, setShowSuccess] = useState(false);
    const [activeTab, setActiveTab] = useState('buy-plans');
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();
    
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isAuthenticated = !!user;

    // Mock active plan for authenticated users
    const activePlan = {
        name: 'Gold Plan',
        expiry: '2025-12-31',
        remaining_data: 'Unlimited',
        status: 'ACTIVE'
    };

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

    const handlePurchaseSuccess = () => {
        setSelectedPlan(null);
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 5000);
    };

    const tabs = [
        { id: 'buy-plans', label: 'Buy Plans', icon: CreditCard, public: true },
        { id: 'my-plans', label: 'My Plans', icon: Wifi, public: true },
        { id: 'usage', label: 'Usage', icon: Activity, public: true },
        { id: 'transactions', label: 'Transactions', icon: LayoutGrid, public: true },
        { id: 'group-plans', label: 'Group Plans', icon: UserPlus, public: true },
        { id: 'support', label: 'Support', icon: MessageSquare, public: true },
    ];

    const filteredTabs = tabs; // Show all tabs regardless of auth

    const renderContent = () => {
        switch (activeTab) {
            case 'buy-plans':
                return (
                    <div className="space-y-8">
                        {/* Header Section */}
                        <div className="text-center max-w-2xl mx-auto mb-12">
                            <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                                {isAuthenticated ? "Buy Data Plans" : "Choose Your Plan"}
                            </h1>
                            <p className="mt-4 text-xl text-gray-500">
                                High-speed internet access tailored to your needs. Instant activation upon payment.
                            </p>
                            {!isAuthenticated && (
                                <div className="mt-8">
                                    <button onClick={() => document.getElementById('plans-grid').scrollIntoView({ behavior: 'smooth' })} className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                                        Get Started
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Features Section (Public Only) */}
                        {!isAuthenticated && (
                            <div className="py-12 bg-white rounded-xl shadow-sm mb-12">
                                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                                    <div className="lg:text-center">
                                        <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">Why Choose ZealNet?</h2>
                                        <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                                            A better way to connect
                                        </p>
                                    </div>

                                    <div className="mt-10">
                                        <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
                                            <div className="relative">
                                                <dt>
                                                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                                                        <Zap className="h-6 w-6" aria-hidden="true" />
                                                    </div>
                                                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Blazing Fast Speeds</p>
                                                </dt>
                                                <dd className="mt-2 ml-16 text-base text-gray-500">
                                                    Experience buffer-free streaming and low-latency gaming with our optimized network.
                                                </dd>
                                            </div>

                                            <div className="relative">
                                                <dt>
                                                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                                                        <Shield className="h-6 w-6" aria-hidden="true" />
                                                    </div>
                                                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Secure & Reliable</p>
                                                </dt>
                                                <dd className="mt-2 ml-16 text-base text-gray-500">
                                                    Your connection is encrypted and monitored 24/7 to ensure maximum uptime and security.
                                                </dd>
                                            </div>

                                            <div className="relative">
                                                <dt>
                                                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                                                        <Check className="h-6 w-6" aria-hidden="true" />
                                                    </div>
                                                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Affordable Plans</p>
                                                </dt>
                                                <dd className="mt-2 ml-16 text-base text-gray-500">
                                                    Flexible pricing options that fit your budget, from daily bundles to monthly unlimited access.
                                                </dd>
                                            </div>

                                            <div className="relative">
                                                <dt>
                                                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                                                        <Wifi className="h-6 w-6" aria-hidden="true" />
                                                    </div>
                                                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Wide Coverage</p>
                                                </dt>
                                                <dd className="mt-2 ml-16 text-base text-gray-500">
                                                    Stay connected across the entire campus/estate with our extensive hotspot network.
                                                </dd>
                                            </div>
                                        </dl>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Plans Grid */}
                        <div id="plans-grid" className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                            {plans.map((plan) => (
                                <Card key={plan.id} className="flex flex-col h-full hover:shadow-lg transition-shadow duration-300 border border-gray-100 relative overflow-hidden">
                                    {/* Best Value Badge (Mock logic) */}
                                    {plan.price === '1000.00' && (
                                        <div className="absolute top-0 right-0 bg-yellow-400 text-yellow-900 text-xs font-bold px-3 py-1 rounded-bl-lg">
                                            BEST VALUE
                                        </div>
                                    )}
                                    
                                    <div className="p-6 flex-1">
                                        <div className="flex items-center justify-between">
                                            <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                                            <div className="p-2 bg-indigo-50 rounded-full">
                                                <Wifi className="h-6 w-6 text-indigo-600" />
                                            </div>
                                        </div>
                                        <div className="mt-4 flex items-baseline text-gray-900">
                                            <span className="text-4xl font-extrabold tracking-tight">{plan.price}</span>
                                            <span className="ml-1 text-xl font-semibold text-gray-500">KES</span>
                                        </div>
                                        <p className="mt-1 text-sm text-gray-500">Per {plan.duration_minutes} Minutes</p>

                                        <ul className="mt-6 space-y-4">
                                            <li className="flex items-start">
                                                <div className="flex-shrink-0">
                                                    <Zap className="h-5 w-5 text-green-500" />
                                                </div>
                                                <p className="ml-3 text-sm text-gray-700">
                                                    Up to <span className="font-semibold">{plan.speed_limit}</span> Speed
                                                </p>
                                            </li>
                                            <li className="flex items-start">
                                                <div className="flex-shrink-0">
                                                    <Clock className="h-5 w-5 text-green-500" />
                                                </div>
                                                <p className="ml-3 text-sm text-gray-700">
                                                    {plan.duration_minutes} Minutes Access
                                                </p>
                                            </li>
                                            <li className="flex items-start">
                                                <div className="flex-shrink-0">
                                                    <Shield className="h-5 w-5 text-green-500" />
                                                </div>
                                                <p className="ml-3 text-sm text-gray-700">Secure Connection</p>
                                            </li>
                                        </ul>
                                    </div>
                                    <div className="p-6 bg-gray-50 border-t border-gray-100 rounded-b-lg">
                                        <Button
                                            className="w-full text-lg py-3"
                                            onClick={() => setSelectedPlan(plan)}
                                        >
                                            Buy Now
                                        </Button>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    </div>
                );
            case 'my-plans':
                return (
                    <div className="mb-12">
                        <Card className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h2 className="text-lg font-semibold opacity-90">Current Active Plan</h2>
                                    <div className="mt-2 flex items-baseline">
                                        <span className="text-3xl font-bold">{activePlan.name}</span>
                                        <span className="ml-2 text-sm opacity-75 bg-green-400 text-green-900 px-2 py-0.5 rounded-full">
                                            {activePlan.status}
                                        </span>
                                    </div>
                                    <p className="mt-1 opacity-75">Expires on {activePlan.expiry}</p>
                                </div>
                                <div className="p-3 bg-white bg-opacity-20 rounded-lg">
                                    <Wifi className="h-8 w-8 text-white" />
                                </div>
                            </div>
                        </Card>
                    </div>
                );
            case 'usage':
                return <Usage />;
            case 'transactions':
                return <Transactions />;
            case 'group-plans':
                return <SocialBilling />;
            case 'support':
                return <Support />;
            default:
                return null;
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Header */}
            <div className="bg-white shadow-sm sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        {/* Logo */}
                        <div className="flex items-center flex-shrink-0 cursor-pointer" onClick={() => setActiveTab('buy-plans')}>
                            <Wifi className="h-8 w-8 text-indigo-600" />
                            <h1 className="ml-2 text-xl font-bold text-gray-900">ZealNet</h1>
                        </div>

                        {/* Desktop Navigation */}
                        <div className="hidden md:flex space-x-8">
                            {filteredTabs.map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`text-sm font-medium transition-colors duration-200 ${
                                        activeTab === tab.id ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-900'
                                    }`}
                                >
                                    {tab.label}
                                </button>
                            ))}
                        </div>

                        {/* User Actions & Mobile Menu Button */}
                        <div className="flex items-center space-x-4">
                            <div className="hidden md:flex items-center space-x-4">
                                {!isAuthenticated ? (
                                    <Button variant="outline" size="sm" onClick={() => navigate('/login')}>
                                        Sign In
                                    </Button>
                                ) : (
                                    <div className="flex items-center space-x-4">
                                         <span className="text-sm text-gray-700">Hi, {user.username}</span>
                                         <Button variant="outline" size="sm" onClick={() => {
                                             localStorage.removeItem('access_token');
                                             localStorage.removeItem('refresh_token');
                                             localStorage.removeItem('user');
                                             navigate('/shop');
                                             window.location.reload();
                                         }}>
                                            Sign Out
                                         </Button>
                                    </div>
                                )}
                            </div>

                            {/* Mobile Menu Button */}
                            <div className="md:hidden">
                                <button
                                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                                    className="text-gray-500 hover:text-gray-900 focus:outline-none"
                                >
                                    {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Mobile Menu Dropdown */}
                {isMenuOpen && (
                    <div className="md:hidden bg-white border-t border-gray-100">
                        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                            {filteredTabs.map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => {
                                        setActiveTab(tab.id);
                                        setIsMenuOpen(false);
                                    }}
                                    className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${
                                        activeTab === tab.id
                                            ? 'bg-indigo-50 text-indigo-600'
                                            : 'text-gray-700 hover:text-gray-900 hover:bg-gray-50'
                                    }`}
                                >
                                    <div className="flex items-center">
                                        <tab.icon className="h-5 w-5 mr-3" />
                                        {tab.label}
                                    </div>
                                </button>
                            ))}
                            <div className="border-t border-gray-100 mt-4 pt-4">
                                {!isAuthenticated ? (
                                    <Button className="w-full justify-center" onClick={() => navigate('/login')}>
                                        Sign In
                                    </Button>
                                ) : (
                                    <div className="space-y-3 px-3">
                                        <p className="text-sm text-gray-500">Signed in as {user.username}</p>
                                        <Button variant="outline" className="w-full justify-center" onClick={() => {
                                             localStorage.removeItem('access_token');
                                             localStorage.removeItem('refresh_token');
                                             localStorage.removeItem('user');
                                             navigate('/shop');
                                             window.location.reload();
                                         }}>
                                            Sign Out
                                         </Button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Main Content */}
            <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Success Message */}
                {showSuccess && (
                    <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-6 mx-auto max-w-3xl">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <Check className="h-5 w-5 text-green-400" />
                            </div>
                            <div className="ml-3">
                                <p className="text-sm text-green-700">
                                    Payment initiated! Please check your phone to complete the transaction.
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {renderContent()}

                {selectedPlan && (
                    <PaymentModal
                        plan={selectedPlan}
                        onClose={() => setSelectedPlan(null)}
                        onSuccess={handlePurchaseSuccess}
                    />
                )}
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 mt-auto">
                <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
                    <div className="md:flex md:items-center md:justify-between">
                        <div className="flex justify-center space-x-6 md:order-2">
                            <a href="#" className="text-gray-400 hover:text-gray-500">
                                <span className="sr-only">Facebook</span>
                                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                                </svg>
                            </a>
                            <a href="#" className="text-gray-400 hover:text-gray-500">
                                <span className="sr-only">Twitter</span>
                                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                                </svg>
                            </a>
                        </div>
                        <div className="mt-8 md:mt-0 md:order-1">
                            <p className="text-center text-base text-gray-400">
                                &copy; 2025 ZealNet HotSpot. All rights reserved.
                            </p>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Shop;
