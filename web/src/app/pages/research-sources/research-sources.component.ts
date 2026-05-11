import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarketIntelligenceService } from '../../core/services/market-intelligence.service';
import { ResearchSource } from '../../core/models/market-intelligence.model';

@Component({
  selector: 'app-research-sources',
  standalone: true,
  imports: [NgIf, NgFor, FormsModule],
  templateUrl: './research-sources.component.html',
  styleUrl: './research-sources.component.scss'
})
export class ResearchSourcesComponent implements OnInit {
  sources: ResearchSource[] = [];
  loading = true;
  error = '';

  selectedSourceType = 'All';
  limit = 50;

  sourceTypes = [
    'All',
    'Patent Reference',
    'Academic Literature',
    'Industry White Paper',
    'Market Report',
    'Technical Article',
    'Vendor Documentation',
    'Competitor Product Release',
    'News Update',
    'Standards Documentation'
  ];

  constructor(private api: MarketIntelligenceService) {}

  ngOnInit(): void {
    this.loadSources();
  }

  loadSources(): void {
    this.loading = true;
    this.error = '';

    const sourceType =
      this.selectedSourceType === 'All' ? undefined : this.selectedSourceType;

    this.api.getResearchSources(this.limit, sourceType).subscribe({
      next: (res) => {
        this.sources = res.data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load research source intelligence.';
        this.loading = false;
      }
    });
  }

  reliabilityClass(score: number): string {
    if (score >= 9) return 'reliability excellent';
    if (score >= 7) return 'reliability good';
    if (score >= 5) return 'reliability medium';
    return 'reliability low';
  }
}