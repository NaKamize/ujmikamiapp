import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-wave">
        <svg viewBox="0 0 1440 60" width="100%" height="60" preserveAspectRatio="none" aria-hidden="true">
          <path fill="#0f172a" d="M0,20 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" />
        </svg>
      </div>

      <div className="footer-inner">
        <div className="footer-brand">
          <span className="footer-name">Jozef Makiš</span>
          <span className="footer-tagline">Software developer, researcher, tinkerer.</span>
        </div>

        <nav className="footer-links" aria-label="Footer navigation">
          <a href="https://www.linkedin.com/in/jozef-maki%C5%A1-05a406251/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="https://github.com/NaKamize" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://arxiv.org/abs/2507.15314" target="_blank" rel="noopener noreferrer">arXiv</a>
          <a href="https://greasyfork.org/en/scripts/468760-grepolisbot" target="_blank" rel="noopener noreferrer">GreasyFork</a>
          <a href="mailto:makisjozef28@gmail.com">Email</a>
        </nav>
      </div>

      <div className="footer-bottom">
        <span>© {new Date().getFullYear()} Jozef Makiš</span>
        <span className="footer-dot">·</span>
        <span>Built with React &amp; TypeScript</span>
      </div>
    </footer>
  );
}
