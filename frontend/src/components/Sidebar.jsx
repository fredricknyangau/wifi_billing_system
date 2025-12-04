import { Link, useLocation } from 'react-router-dom';
import { Home, Users, CreditCard, Ticket, Settings, LogOut, Wifi, Activity, X, MessageSquare, UserPlus } from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
    const location = useLocation();

    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const isCustomer = user.is_customer;

    const allLinks = [
        { name: 'Dashboard', path: '/', icon: Home, roles: ['admin'] },
        { name: 'Buy Plans', path: '/buy-plans', icon: CreditCard, roles: ['customer'] },
        { name: 'My Plans', path: '/my-plans', icon: Wifi, roles: ['customer'] },
        { name: 'Plans', path: '/plans', icon: CreditCard, roles: ['admin'] },
        { name: 'Vouchers', path: '/vouchers', icon: Ticket, roles: ['admin'] },
        { name: 'Customers', path: '/customers', icon: Users, roles: ['admin'] },
        { name: 'Transactions', path: '/Transactions', icon: Activity, roles: ['admin'] },
    ];

    const isAdmin = user.is_staff || user.is_superuser;

    const links = allLinks.filter(link => {
        if (isAdmin) return link.roles.includes('admin');
        return link.roles.includes('customer');
    });

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    };

    const sidebarContent = (
        <div className="h-full flex flex-col bg-gray-900 text-white shadow-xl">
            <div className="h-16 flex items-center justify-between px-6 bg-gray-800 border-b border-gray-700">
                <div className="flex items-center">
                    <Wifi className="w-6 h-6 text-indigo-500 mr-3" />
                    <h1 className="text-xl font-bold tracking-tight">ZealNet WiFi Billing System</h1>
                </div>
                {/* Close button for mobile */}
                <button
                    onClick={onClose}
                    className="md:hidden p-2 rounded-md text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
                >
                    <X className="h-6 w-6" />
                </button>
            </div>

            <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
                {links.map((link) => {
                    const Icon = link.icon;
                    const isActive = location.pathname === link.path;
                    return (
                        <Link
                            key={link.path}
                            to={link.path}
                            onClick={onClose} // Close sidebar on link click (mobile)
                            className={`group flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-all duration-200 ${isActive
                                ? 'bg-indigo-600 text-white shadow-md'
                                : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                }`}
                        >
                            <Icon className={`w-5 h-5 mr-3 flex-shrink-0 transition-colors ${isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'
                                }`} />
                            {link.name}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-gray-800 bg-gray-900">
                <button
                    onClick={handleLogout}
                    className="flex items-center w-full px-3 py-2.5 text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-800 rounded-md transition-colors"
                >
                    <LogOut className="w-5 h-5 mr-3" />
                    Sign Out
                </button>
            </div>
        </div>
    );

    return (
        <>
            {/* Mobile Overlay */}
            <div
                className={`fixed inset-0 z-40 bg-gray-600 bg-opacity-75 transition-opacity duration-300 ease-linear md:hidden ${isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
                    }`}
                onClick={onClose}
                aria-hidden="true"
            ></div>

            {/* Sidebar Container */}
            <div
                className={`fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:inset-auto md:flex md:flex-col ${isOpen ? 'translate-x-0' : '-translate-x-full'
                    }`}
            >
                {sidebarContent}
            </div>
        </>
    );
};

export default Sidebar;
