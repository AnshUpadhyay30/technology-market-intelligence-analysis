import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Competitor,
  ResearchSource,
  Summary,
  Technology
} from '../models/market-intelligence.model';

@Injectable({
  providedIn: 'root'
})
export class MarketIntelligenceService {
  private readonly baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  getSummary(): Observable<{ status: string; summary: Summary }> {
    return this.http.get<{ status: string; summary: Summary }>(
      `${this.baseUrl}/api/summary`
    );
  }

  getTechnologies(
    limit = 10,
    priority?: string,
    category?: string
  ): Observable<{ status: string; count: number; data: Technology[] }> {
    let params = new HttpParams().set('limit', limit);

    if (priority && priority !== 'All') {
      params = params.set('priority', priority);
    }

    if (category && category !== 'All') {
      params = params.set('category', category);
    }

    return this.http.get<{ status: string; count: number; data: Technology[] }>(
      `${this.baseUrl}/api/technologies`,
      { params }
    );
  }

  getCompetitors(): Observable<{ status: string; count: number; data: Competitor[] }> {
    return this.http.get<{ status: string; count: number; data: Competitor[] }>(
      `${this.baseUrl}/api/competitors`
    );
  }

  getResearchSources(
    limit = 50,
    sourceType?: string
  ): Observable<{ status: string; count: number; data: ResearchSource[] }> {
    let params = new HttpParams().set('limit', limit);

    if (sourceType && sourceType !== 'All') {
      params = params.set('source_type', sourceType);
    }

    return this.http.get<{ status: string; count: number; data: ResearchSource[] }>(
      `${this.baseUrl}/api/research-sources`,
      { params }
    );
  }

  runAnalysis(): Observable<any> {
    return this.http.post(`${this.baseUrl}/api/run-analysis`, {});
  }

  downloadReport(): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/api/download-report`, {
      responseType: 'blob'
    });
  }
}