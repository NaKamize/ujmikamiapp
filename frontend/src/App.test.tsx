import { render, screen } from '@testing-library/react';
import App from './App';

beforeEach(() => {
  jest.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('network disabled in tests'));
});

afterEach(() => {
  jest.restoreAllMocks();
});

test('renders the hero heading with the site owner name', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /jozef makiš/i, level: 1 })).toBeInTheDocument();
});

test('renders navbar section buttons', () => {
  render(<App />);
  expect(screen.getByRole('button', { name: /about/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /projects/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /ml showcase/i })).toBeInTheDocument();
});
