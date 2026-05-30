import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BookOpen, BarChart3, Bookmark, Home } from 'lucide-react';

export const Navigation: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 bg-gradient-to-r from-purple-600 via-purple-700 to-indigo-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="p-2 bg-white rounded-lg group-hover:scale-110 transition-transform">
              <BookOpen className="w-6 h-6 text-purple-600" />
            </div>
            <span className="text-white font-bold text-xl hidden sm:inline">
              My Library
            </span>
          </Link>

          <div className="flex items-center space-x-1 md:space-x-2">
            <NavLink
              to="/"
              icon={<Home className="w-5 h-5" />}
              label="Home"
              active={isActive('/')}
            />
            <NavLink
              to="/statistics"
              icon={<BarChart3 className="w-5 h-5" />}
              label="Stats"
              active={isActive('/statistics')}
            />
            <NavLink
              to="/tbr"
              icon={<Bookmark className="w-5 h-5" />}
              label="TBR"
              active={isActive('/tbr')}
            />
          </div>
        </div>
      </div>
    </nav>
  );
};

interface NavLinkProps {
  to: string;
  icon: React.ReactNode;
  label: string;
  active: boolean;
}

const NavLink: React.FC<NavLinkProps> = ({ to, icon, label, active }) => (
  <Link
    to={to}
    className={`p-3 rounded-lg flex items-center space-x-2 transition-all ${
      active
        ? 'bg-white text-purple-600 shadow-lg'
        : 'text-white hover:bg-white/20'
    }`}
  >
    {icon}
    <span className="hidden md:inline text-sm font-medium">{label}</span>
  </Link>
);
