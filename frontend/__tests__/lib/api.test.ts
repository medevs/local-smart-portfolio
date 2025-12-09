import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock API client for testing
class MockApiClient {
  private baseUrl: string
  private adminKey: string | undefined

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    this.adminKey = process.env.NEXT_PUBLIC_ADMIN_API_KEY
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (this.adminKey) {
      headers['X-Admin-Key'] = this.adminKey
    }
    return headers
  }

  async getHealth() {
    const response = await fetch(`${this.baseUrl}/health`)
    if (!response.ok) throw new Error('Health check failed')
    return response.json()
  }

  async getSystemMetrics() {
    const response = await fetch(`${this.baseUrl}/metrics/system`)
    if (!response.ok) throw new Error('Failed to fetch metrics')
    return response.json()
  }

  async getBenchmarks() {
    const response = await fetch(`${this.baseUrl}/metrics/benchmarks`)
    if (!response.ok) throw new Error('Failed to fetch benchmarks')
    return response.json()
  }

  async uploadDocument(file: File) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${this.baseUrl}/ingest`, {
      method: 'POST',
      headers: { 'X-Admin-Key': this.adminKey || '' },
      body: formData,
    })
    if (!response.ok) throw new Error('Upload failed')
    return response.json()
  }

  async getDocuments() {
    const response = await fetch(`${this.baseUrl}/admin/documents`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch documents')
    return response.json()
  }

  async deleteDocument(documentId: string) {
    const response = await fetch(`${this.baseUrl}/admin/documents/${documentId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error('Delete failed')
    return response.json()
  }

  async getStats() {
    const response = await fetch(`${this.baseUrl}/admin/stats`, {
      headers: this.getHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch stats')
    return response.json()
  }
}

describe('ApiClient', () => {
  let api: MockApiClient
  let mockFetch: ReturnType<typeof vi.fn>

  beforeEach(() => {
    api = new MockApiClient()
    mockFetch = vi.fn()
    global.fetch = mockFetch
  })

  describe('getHealth', () => {
    it('fetches health status from correct endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            status: 'healthy',
            version: '1.0.0',
            services: { ollama: 'connected', chromadb: 'connected' },
          }),
      })

      const result = await api.getHealth()

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/health')
      expect(result.status).toBe('healthy')
    })

    it('throws error on failed health check', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      await expect(api.getHealth()).rejects.toThrow('Health check failed')
    })
  })

  describe('getSystemMetrics', () => {
    it('fetches system metrics from correct endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            cpu_percent: 25.5,
            ram_used_gb: 8.2,
            ram_total_gb: 16,
            uptime_days: 5,
          }),
      })

      const result = await api.getSystemMetrics()

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/metrics/system')
      expect(result.cpu_percent).toBe(25.5)
    })
  })

  describe('getBenchmarks', () => {
    it('fetches benchmarks from correct endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            benchmarks: [
              {
                model: 'llama3.2:3b',
                tokens_per_second: 25.5,
                memory_gb: 4.2,
                latency_ms: 150,
                quality_score: 0.85,
              },
            ],
            timestamp: '2024-01-01T00:00:00Z',
          }),
      })

      const result = await api.getBenchmarks()

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/metrics/benchmarks')
      expect(result.benchmarks).toHaveLength(1)
    })
  })

  describe('uploadDocument', () => {
    it('uploads document with correct headers', async () => {
      const file = new File(['test content'], 'test.md', { type: 'text/markdown' })

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            success: true,
            document_id: 'doc_123',
            chunks: 5,
          }),
      })

      const result = await api.uploadDocument(file)

      expect(mockFetch).toHaveBeenCalled()
      const [url, options] = mockFetch.mock.calls[0]
      expect(url).toBe('http://localhost:8000/ingest')
      expect(options.method).toBe('POST')
      expect(options.body).toBeInstanceOf(FormData)
    })

    it('throws error on upload failure', async () => {
      const file = new File(['test'], 'test.md', { type: 'text/markdown' })

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
      })

      await expect(api.uploadDocument(file)).rejects.toThrow('Upload failed')
    })
  })

  describe('getDocuments', () => {
    it('fetches documents with admin key header', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            documents: [
              { id: 'doc_1', filename: 'test.md', chunk_count: 5 },
            ],
            total_count: 1,
          }),
      })

      await api.getDocuments()

      const [url, options] = mockFetch.mock.calls[0]
      expect(url).toBe('http://localhost:8000/admin/documents')
      expect(options.headers['X-Admin-Key']).toBeDefined()
    })
  })

  describe('deleteDocument', () => {
    it('deletes document with correct endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            success: true,
            message: 'Document deleted',
          }),
      })

      await api.deleteDocument('doc_123')

      const [url, options] = mockFetch.mock.calls[0]
      expect(url).toBe('http://localhost:8000/admin/documents/doc_123')
      expect(options.method).toBe('DELETE')
    })
  })

  describe('getStats', () => {
    it('fetches stats from admin endpoint', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            total_documents: 10,
            total_chunks: 100,
            embedding_model: 'nomic-embed-text',
          }),
      })

      const result = await api.getStats()

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/admin/stats',
        expect.objectContaining({
          headers: expect.objectContaining({
            'X-Admin-Key': expect.any(String),
          }),
        })
      )
      expect(result.total_documents).toBe(10)
    })
  })
})

describe('API Error Handling', () => {
  let api: MockApiClient
  let mockFetch: ReturnType<typeof vi.fn>

  beforeEach(() => {
    api = new MockApiClient()
    mockFetch = vi.fn()
    global.fetch = mockFetch
  })

  it('handles network errors gracefully', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    await expect(api.getHealth()).rejects.toThrow('Network error')
  })

  it('handles 500 errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    })

    await expect(api.getHealth()).rejects.toThrow()
  })

  it('handles 401 unauthorized', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
    })

    await expect(api.getDocuments()).rejects.toThrow()
  })

  it('handles 403 forbidden', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 403,
    })

    await expect(api.getStats()).rejects.toThrow()
  })
})
