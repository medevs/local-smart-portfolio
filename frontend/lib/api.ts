/**
 * API client for backend communication.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Admin API key (in production, this should be handled more securely)
const ADMIN_API_KEY = process.env.NEXT_PUBLIC_ADMIN_API_KEY || "dev-admin-key-123";

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
 * API client class
 */
class ApiClient {
  private baseUrl: string;
  private adminKey: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
    this.adminKey = ADMIN_API_KEY;
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

