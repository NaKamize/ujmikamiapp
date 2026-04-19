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
      <h3>{title}</h3>
      <p>{children}</p>
      {stat && <p className="card-stat">{stat}</p>}
      {img && (
        <div>
          <img src={img} alt="" />
        </div>
      )}
      {links && links.length > 0 && (
        <div className="card-links">
          {links.map((l, i) => (
            <a key={i} href={l.url} className="card-link" target="_blank" rel="noopener noreferrer">{l.label}</a>
          ))}
        </div>
      )}
    </div>
  );
}