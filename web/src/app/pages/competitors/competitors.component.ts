import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { MarketIntelligenceService } from '../../core/services/market-intelligence.service';
import { Competitor } from '../../core/models/market-intelligence.model';

@Component({
  selector: 'app-competitors',
  standalone: true,
  imports: [NgIf, NgFor],
  templateUrl: './competitors.component.html',
  styleUrl: './competitors.component.scss'
})
export class CompetitorsComponent implements OnInit {
  competitors: Competitor[] = [];
  loading = true;
  error = '';

  constructor(private api: MarketIntelligenceService) {}

  ngOnInit(): void {
    this.loadCompetitors();
  }

  loadCompetitors(): void {
    this.loading = true;
    this.error = '';

    this.api.getCompetitors().subscribe({
      next: (res) => {
        this.competitors = res.data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load competitor intelligence.';
        this.loading = false;
      }
    });
  }

  adoptionClass(value: number): string {
    if (value >= 27) return 'adoption excellent';
    if (value >= 25) return 'adoption good';
    if (value >= 23) return 'adoption medium';
    return 'adoption low';
  }
}