import './WorkExperience.css';

interface TechBadge {
  label: string;
}

interface WorkExperienceItem {
  id: number;
  company: string;
  role: string;
  period: string;
  location: string;
  description: string;
  technologies: TechBadge[];
  current?: boolean;
}

interface WorkExperienceProps {
  experiences: WorkExperienceItem[];
}

function ExperienceCard({ exp }: { exp: WorkExperienceItem }) {
  return (
    <div className="exp-card">
      <div className="exp-timeline-dot" aria-hidden="true">
        {exp.current && <span className="exp-dot-pulse" />}
      </div>

      <div className="exp-body">
        <div className="exp-header">
          <div className="exp-title-group">
            <h3 className="exp-role">{exp.role}</h3>
            <span className="exp-company">{exp.company}</span>
          </div>
          <div className="exp-meta">
            <span className="exp-period">{exp.period}</span>
            <span className="exp-location">{exp.location}</span>
          </div>
        </div>

        <p className="exp-description">{exp.description}</p>

        {exp.technologies.length > 0 && (
          <ul className="exp-tech-list" aria-label="Technologies used">
            {exp.technologies.map((tech) => (
              <li key={tech.label} className="exp-tech-badge">
                {tech.label}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function WorkExperience({ experiences }: WorkExperienceProps) {
  if (experiences.length === 0) {
    return null;
  }

  return (
    <div className="exp-timeline">
      {experiences.map((exp) => (
        <ExperienceCard key={exp.id} exp={exp} />
      ))}
    </div>
  );
}

export type { WorkExperienceItem };
