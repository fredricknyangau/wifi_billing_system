import React from 'react';

const Card = ({ children, className = '', title, action }) => {
    return (
        <div className={`bg-white overflow-hidden shadow rounded-lg ${className}`}>
            {(title || action) && (
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
                    {title && <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>}
                    {action && <div>{action}</div>}
                </div>
            )}
            <div className="px-4 py-5 sm:p-6">
                {children}
            </div>
        </div>
    );
};

export default Card;
