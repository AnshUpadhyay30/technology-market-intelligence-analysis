import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarketIntelligenceService } from '../../core/services/market-intelligence.service';
import { Technology } from '../../core/models/market-intelligence.model';

@Component({
  selector: 'app-technologies',
  standalone: true,
  imports: [NgIf, NgFor, FormsModule],
  templateUrl: './technologies.component.html',
  styleUrl: './technologies.component.scss'
})
export class TechnologiesComponent implements OnInit {
  technologies: Technology[] = [];
  loading = true;
  error = '';

  selectedPriority = 'All';
  limit = 50;

  priorityOptions = ['All', 'Critical', 'High', 'Medium', 'Low'];

  constructor(private api: MarketIntelligenceService) {}

  ngOnInit(): void {
    this.loadTechnologies();
  }

  loadTechnologies(): void {
    this.loading = true;
    this.error = '';

    const priority =
      this.selectedPriority === 'All' ? undefined : this.selectedPriority;

    this.api.getTechnologies(this.limit, priority).subscribe({
      next: (res) => {
        this.technologies = res.data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load priority report.';
        this.loading = false;
      }
    });
  }

  badgeClass(level: string): string {
    return `priority-badge ${level.toLowerCase()}`;
  }
}