import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { forkJoin } from 'rxjs';
import { MarketIntelligenceService } from '../../core/services/market-intelligence.service';
import { Summary, Technology } from '../../core/models/market-intelligence.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NgIf, NgFor],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  summary?: Summary;
  topTechnologies: Technology[] = [];
  loading = true;
  error = '';

  constructor(private api: MarketIntelligenceService) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.loading = true;
    this.error = '';

    forkJoin({
      summaryRes: this.api.getSummary(),
      techRes: this.api.getTechnologies(10)
    }).subscribe({
      next: ({ summaryRes, techRes }) => {
        this.summary = summaryRes.summary;
        this.topTechnologies = techRes.data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Dashboard load error:', err);
        this.error = 'Unable to load dashboard data.';
        this.loading = false;
      }
    });
  }

  badgeClass(level: string): string {
    return `priority-badge ${level.toLowerCase()}`;
  }
}