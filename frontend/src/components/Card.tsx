import React from 'react';
import './Card.css';

interface CardLink {
  label: string;
  url: string;
}

interface CardProps {
  title: string;
  children: React.ReactNode;
  img?: string;
  links?: CardLink[];
  stat?: string;
}

export default function Card({ title, children, img, links, stat }: CardProps) {
  return (
    <div className="card">
      {img && (
        <div className="card-img-wrapper">
          <img src={img} alt={title} loading="lazy" />
        </div>
      )}

      <div className="card-body">
        <h3>{title}</h3>
        <p>{children}</p>
        {stat && <span className="card-stat">{stat}</span>}
        {links && links.length > 0 && (
          <div className="card-links">
            {links.map((l, i) => (
              <a
                key={i}
                href={l.url}
                className="card-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                {l.label}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
