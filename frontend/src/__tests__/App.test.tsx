/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    expect(screen.getByText('NeuroQuest')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    expect(screen.getByText('Search')).toBeInTheDocument()
    expect(screen.getByText('Knowledge Graph')).toBeInTheDocument()
    expect(screen.getByText('Profile')).toBeInTheDocument()
  })
})
