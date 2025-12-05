import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import PaymentModal from "../components/PaymentModal";
import {
  Wifi,
  Check,
  Zap,
  Clock,
  Shield,
  CreditCard,
  Activity,
  UserPlus,
  MessageSquare,
  LayoutGrid,
  Menu,
  X,
} from "lucide-react";
import Usage from "./Usage";
import Transactions from "./Transactions";
import SocialBilling from "./SocialBilling";
import Support from "./Support";

// ============================================================================
// CONSTANTS & CONFIGURATION
// ============================================================================

const TABS = [
  { id: "buy-plans", label: "Buy Plans", icon: CreditCard, public: true },
  { id: "my-plans", label: "My Plans", icon: Wifi, public: true },
  { id: "usage", label: "Usage", icon: Activity, public: true },
  { id: "transactions", label: "Transactions", icon: LayoutGrid, public: true },
  { id: "group-plans", label: "Group Plans", icon: UserPlus, public: true },
  { id: "support", label: "Support", icon: MessageSquare, public: true },
];

const FEATURES = [
  {
    icon: Zap,
    title: "Blazing Fast Speeds",
    description:
      "Experience buffer-free streaming and low-latency gaming with our optimized network.",
  },
  {
    icon: Shield,
    title: "Secure & Reliable",
    description:
      "Your connection is encrypted and monitored 24/7 to ensure maximum uptime and security.",
  },
  {
    icon: Check,
    title: "Affordable Plans",
    description:
      "Flexible pricing options that fit your budget, from daily bundles to monthly unlimited access.",
  },
  {
    icon: Wifi,
    title: "Wide Coverage",
    description:
      "Stay connected across the entire campus/estate with our extensive hotspot network.",
  },
];

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

const getStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem("user") || "null");
  } catch {
    return null;
  }
};

const clearAuthTokens = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
};

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

const Header = ({
  activeTab,
  setActiveTab,
  isAuthenticated,
  user,
  navigate,
  isMenuOpen,
  setIsMenuOpen,
}) => (
  <div className="sticky top-0 z-50 bg-white shadow-sm">
    <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        {/* Logo */}
        <div
          className="flex items-center flex-shrink-0 cursor-pointer"
          onClick={() => setActiveTab("buy-plans")}
        >
          <Wifi className="w-8 h-8 text-indigo-600" />
          <h1 className="ml-2 text-xl font-bold text-gray-900">ZealNet</h1>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden space-x-8 md:flex">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`text-sm font-medium transition-colors duration-200 ${
                activeTab === tab.id
                  ? "text-indigo-600"
                  : "text-gray-500 hover:text-gray-900"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        {/* User Actions & Mobile Menu Button */}
        <div className="flex items-center space-x-4">
          <div className="items-center hidden space-x-4 md:flex">
            {!isAuthenticated ? (
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate("/login")}
              >
                Sign In
              </Button>
            ) : (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Hi, {user.username}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    clearAuthTokens();
                    navigate("/shop");
                    window.location.reload();
                  }}
                >
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
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>

    {/* Mobile Menu Dropdown */}
    {isMenuOpen && (
      <MobileMenu
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        setIsMenuOpen={setIsMenuOpen}
        isAuthenticated={isAuthenticated}
        user={user}
        navigate={navigate}
      />
    )}
  </div>
);

const MobileMenu = ({
  activeTab,
  setActiveTab,
  setIsMenuOpen,
  isAuthenticated,
  user,
  navigate,
}) => (
  <div className="bg-white border-t border-gray-100 md:hidden">
    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => {
            setActiveTab(tab.id);
            setIsMenuOpen(false);
          }}
          className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${
            activeTab === tab.id
              ? "bg-indigo-50 text-indigo-600"
              : "text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          }`}
        >
          <div className="flex items-center">
            <tab.icon className="w-5 h-5 mr-3" />
            {tab.label}
          </div>
        </button>
      ))}
      <div className="pt-4 mt-4 border-t border-gray-100">
        {!isAuthenticated ? (
          <Button
            className="justify-center w-full"
            onClick={() => navigate("/login")}
          >
            Sign In
          </Button>
        ) : (
          <div className="px-3 space-y-3">
            <p className="text-sm text-gray-500">
              Signed in as {user.username}
            </p>
            <Button
              variant="outline"
              className="justify-center w-full"
              onClick={() => {
                clearAuthTokens();
                navigate("/shop");
                window.location.reload();
              }}
            >
              Sign Out
            </Button>
          </div>
        )}
      </div>
    </div>
  </div>
);

const HeroSection = ({ isAuthenticated }) => (
  <div className="max-w-2xl mx-auto mb-12 text-center">
    <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
      {isAuthenticated ? "Buy Data Plans" : "Choose Your Plan"}
    </h1>
    <p className="mt-4 text-xl text-gray-500">
      High-speed internet access tailored to your needs. Instant activation upon
      payment.
    </p>
    {!isAuthenticated && (
      <div className="mt-8">
        <button
          onClick={() =>
            document
              .getElementById("plans-grid")
              ?.scrollIntoView({ behavior: "smooth" })
          }
          className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700"
        >
          Get Started
        </button>
      </div>
    )}
  </div>
);

const FeaturesSection = () => (
  <div className="py-12 mb-12 bg-white shadow-sm rounded-xl">
    <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div className="lg:text-center">
        <h2 className="text-base font-semibold tracking-wide text-indigo-600 uppercase">
          Why Choose ZealNet?
        </h2>
        <p className="mt-2 text-3xl font-extrabold leading-8 tracking-tight text-gray-900 sm:text-4xl">
          A better way to connect
        </p>
      </div>

      <div className="mt-10">
        <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          {FEATURES.map((feature) => (
            <div key={feature.title} className="relative">
              <dt>
                <div className="absolute flex items-center justify-center w-12 h-12 text-white bg-indigo-500 rounded-md">
                  <feature.icon className="w-6 h-6" aria-hidden="true" />
                </div>
                <p className="ml-16 text-lg font-medium leading-6 text-gray-900">
                  {feature.title}
                </p>
              </dt>
              <dd className="mt-2 ml-16 text-base text-gray-500">
                {feature.description}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  </div>
);

const PlanCard = ({ plan, onSelect }) => {
  const isBestValue = plan.price === "1000.00";

  return (
    <Card className="relative flex flex-col h-full overflow-hidden transition-shadow duration-300 border border-gray-100 hover:shadow-lg">
      {isBestValue && (
        <div className="absolute top-0 right-0 px-3 py-1 text-xs font-bold text-yellow-900 bg-yellow-400 rounded-bl-lg">
          BEST VALUE
        </div>
      )}

      <div className="flex-1 p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
          <div className="p-2 rounded-full bg-indigo-50">
            <Wifi className="w-6 h-6 text-indigo-600" />
          </div>
        </div>

        <div className="flex items-baseline mt-4 text-gray-900">
          <span className="text-4xl font-extrabold tracking-tight">
            {plan.price}
          </span>
          <span className="ml-1 text-xl font-semibold text-gray-500">KES</span>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Per {plan.duration_minutes} Minutes
        </p>

        <ul className="mt-6 space-y-4">
          <li className="flex items-start">
            <Zap className="flex-shrink-0 w-5 h-5 text-green-500" />
            <p className="ml-3 text-sm text-gray-700">
              Up to <span className="font-semibold">{plan.speed_limit}</span>{" "}
              Speed
            </p>
          </li>
          <li className="flex items-start">
            <Clock className="flex-shrink-0 w-5 h-5 text-green-500" />
            <p className="ml-3 text-sm text-gray-700">
              {plan.duration_minutes} Minutes Access
            </p>
          </li>
          <li className="flex items-start">
            <Shield className="flex-shrink-0 w-5 h-5 text-green-500" />
            <p className="ml-3 text-sm text-gray-700">Secure Connection</p>
          </li>
        </ul>
      </div>

      <div className="p-6 border-t border-gray-100 rounded-b-lg bg-gray-50">
        <Button className="w-full py-3 text-lg" onClick={() => onSelect(plan)}>
          Buy Now
        </Button>
      </div>
    </Card>
  );
};

const ActivePlanCard = ({ plan }) => (
  <Card className="mb-12 text-white bg-gradient-to-r from-indigo-600 to-purple-600">
    <div className="flex items-center justify-between">
      <div>
        <h2 className="text-lg font-semibold opacity-90">
          Current Active Plan
        </h2>
        <div className="flex items-baseline mt-2">
          <span className="text-3xl font-bold">{plan.name}</span>
          <span className="ml-2 text-sm opacity-75 bg-green-400 text-green-900 px-2 py-0.5 rounded-full">
            {plan.status}
          </span>
        </div>
        <p className="mt-1 opacity-75">Expires on {plan.expiry}</p>
      </div>
      <div className="p-3 bg-white rounded-lg bg-opacity-20">
        <Wifi className="w-8 h-8 text-white" />
      </div>
    </div>
  </Card>
);

const SuccessAlert = () => (
  <div className="max-w-3xl p-4 mx-auto mb-6 border-l-4 border-green-400 bg-green-50">
    <div className="flex">
      <Check className="flex-shrink-0 w-5 h-5 text-green-400" />
      <div className="ml-3">
        <p className="text-sm text-green-700">
          Payment initiated! Please check your phone to complete the
          transaction.
        </p>
      </div>
    </div>
  </div>
);

const Footer = () => (
  <footer className="mt-auto bg-white border-t border-gray-200">
    <div className="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div className="md:flex md:items-center md:justify-between">
        <div className="flex justify-center space-x-6 md:order-2">
          <a href="#" className="text-gray-400 hover:text-gray-500">
            <span className="sr-only">Facebook</span>
            <svg
              className="w-6 h-6"
              fill="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"
                clipRule="evenodd"
              />
            </svg>
          </a>
          <a href="#" className="text-gray-400 hover:text-gray-500">
            <span className="sr-only">Twitter</span>
            <svg
              className="w-6 h-6"
              fill="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
            </svg>
          </a>
        </div>
        <div className="mt-8 md:mt-0 md:order-1">
          <p className="text-base text-center text-gray-400">
            &copy; 2025 ZealNet HotSpot. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  </footer>
);

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const Shop = () => {
  // State
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState("buy-plans");
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigate = useNavigate();
  const user = getStoredUser();
  const isAuthenticated = !!user;

  // Mock active plan for authenticated users
  const activePlan = {
    name: "Gold Plan",
    expiry: "2025-12-31",
    remaining_data: "Unlimited",
    status: "ACTIVE",
  };

  // Fetch plans on mount
  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await api.get("/billing/plans/");
        setPlans(response.data);
      } catch (error) {
        console.error("Failed to fetch plans", error);
      }
    };

    fetchPlans();
  }, []);

  // Handlers
  const handlePurchaseSuccess = () => {
    setSelectedPlan(null);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 5000);
  };

  // Render tab content
  const renderContent = () => {
    switch (activeTab) {
      case "buy-plans":
        return (
          <div className="space-y-8">
            <HeroSection isAuthenticated={isAuthenticated} />
            {!isAuthenticated && <FeaturesSection />}
            <div
              id="plans-grid"
              className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
            >
              {plans.map((plan) => (
                <PlanCard
                  key={plan.id}
                  plan={plan}
                  onSelect={setSelectedPlan}
                />
              ))}
            </div>
          </div>
        );
      case "my-plans":
        return <ActivePlanCard plan={activePlan} />;
      case "usage":
        return <Usage />;
      case "transactions":
        return <Transactions />;
      case "group-plans":
        return <SocialBilling />;
      case "support":
        return <Support />;
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isAuthenticated={isAuthenticated}
        user={user}
        navigate={navigate}
        isMenuOpen={isMenuOpen}
        setIsMenuOpen={setIsMenuOpen}
      />

      <main className="flex-grow w-full px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
        {showSuccess && <SuccessAlert />}
        {renderContent()}
        {selectedPlan && (
          <PaymentModal
            plan={selectedPlan}
            onClose={() => setSelectedPlan(null)}
            onSuccess={handlePurchaseSuccess}
          />
        )}
      </main>

      <Footer />
    </div>
  );
};

export default Shop;
