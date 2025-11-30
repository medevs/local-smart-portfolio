/**
 * API client for backend communication.
 * 
 * Security Note:
 * - API keys are loaded from environment variables
 * - Never hardcode API keys in source code
 * - Set NEXT_PUBLIC_ADMIN_API_KEY in .env.local
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL as string;

// Admin API key from environment (required for admin operations)
const ADMIN_API_KEY = process.env.NEXT_PUBLIC_ADMIN_API_KEY || "";

/**
 * Check if admin API key is configured
 */
export function isAdminKeyConfigured(): boolean {
  return Boolean(ADMIN_API_KEY && ADMIN_API_KEY.length >= 16);
}

/**
 * Document metadata from the API
 */
export interface DocumentInfo {
  document_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  chunk_count: number;
  uploaded_at: string;
}

/**
 * Upload response from the API
 */
export interface UploadResponse {
  success: boolean;
  message?: string;
  document?: {
    id: string;
    filename: string;
    file_type: string;
    file_size: number;
    chunk_count: number;
    uploaded_at: string;
  };
  error?: string;
}

/**
 * Knowledge base statistics
 */
export interface KBStats {
  total_documents: number;
  total_chunks: number;
  embedding_model: string;
}

/**
 * Health status response
 */
export interface HealthStatus {
  status: string;
  version: string;
  timestamp: string;
  services: {
    ollama: string;
    chromadb: string;
  };
}

/**
 * Get the current admin API key from session storage or environment
 */
function getAdminKey(): string {
  // First check session storage (set during login)
  if (typeof window !== "undefined") {
    const sessionKey = sessionStorage.getItem("admin_api_key");
    if (sessionKey) return sessionKey;
  }
  // Fall back to environment variable
  return ADMIN_API_KEY;
}

/**
 * API client class
 */
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  /**
   * Get the current admin API key
   */
  private get adminKey(): string {
    return getAdminKey();
  }

  /**
   * Get health status
   */
  async getHealth(): Promise<HealthStatus> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error("Failed to get health status");
    return response.json();
  }

  /**
   * Upload a document (uses /ingest endpoint)
   */
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseUrl}/ingest`, {
      method: "POST",
      headers: {
        "X-Admin-Key": this.adminKey,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to upload document");
    }

    return response.json();
  }

  /**
   * Get list of all documents (uses /admin/documents endpoint)
   */
  async getDocuments(): Promise<DocumentInfo[]> {
    const response = await fetch(`${this.baseUrl}/admin/documents`, {
      headers: {
        "X-Admin-Key": this.adminKey,
      },
    });

    if (!response.ok) throw new Error("Failed to get documents");
    
    // Transform the response to match expected format
    const data = await response.json();
    return (data.documents || []).map((doc: { id: string; filename: string; file_type: string; file_size: number; chunk_count: number; uploaded_at: string }) => ({
      document_id: doc.id,
      filename: doc.filename,
      file_type: doc.file_type,
      file_size: doc.file_size,
      chunk_count: doc.chunk_count,
      uploaded_at: doc.uploaded_at,
    }));
  }

  /**
   * Delete a document (uses /admin/documents endpoint)
   */
  async deleteDocument(documentId: string): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${this.baseUrl}/admin/documents/${documentId}`, {
      method: "DELETE",
      headers: {
        "X-Admin-Key": this.adminKey,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to delete document");
    }

    return response.json();
  }

  /**
   * Get knowledge base statistics (uses /admin/stats endpoint)
   */
  async getStats(): Promise<KBStats> {
    const response = await fetch(`${this.baseUrl}/admin/stats`, {
      headers: {
        "X-Admin-Key": this.adminKey,
      },
    });

    if (!response.ok) throw new Error("Failed to get stats");
    return response.json();
  }
}

// Export singleton instance
export const api = new ApiClient();

