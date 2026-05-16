import { useEffect, useState } from 'react';
import './Navbar.css';

interface NavbarProps {
  links: { id: string; label: string }[];
}

export default function Navbar({ links }: NavbarProps) {
  const [scrolled, setScrolled] = useState(false);
  const [activeId, setActiveId] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);

      // Determine active section
      const scrollPos = window.scrollY + 100;
      let current = '';
      for (const link of links) {
        const el = document.getElementById(link.id);
        if (el && el.offsetTop <= scrollPos) {
          current = link.id;
        }
      }
      setActiveId(current);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [links]);

  const handleClick = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      const navH = 64;
      const top = el.getBoundingClientRect().top + window.scrollY - navH;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  };

  return (
    <nav className={`navbar${scrolled ? ' navbar-scrolled' : ''}`}>
      <div className="navbar-inner">
        <span className="navbar-brand">Jozef Makiš</span>
        <div className="navbar-links">
          {links.map((link) => (
            <button
              key={link.id}
              className={`navbar-link${activeId === link.id ? ' active' : ''}`}
              onClick={() => handleClick(link.id)}
            >
              {link.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}
