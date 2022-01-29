import {Component, OnInit, ViewChild} from '@angular/core';
import {Car} from "../model/car";
import {MatTableDataSource} from "@angular/material/table";
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";
import {CarService} from "../car.service";
import {MatDialog} from "@angular/material/dialog";
import {CarAddComponent} from "./car-add/car-add.component";

@Component({
  selector: 'app-car-management',
  templateUrl: './car-management.component.html',
  styleUrls: ['./car-management.component.css']
})
export class CarManagementComponent implements OnInit {

  dataSource!: MatTableDataSource<Car>;
  displayedColumns: string[] = ['licensePlate', 'width', 'length', 'hasAccess', 'changeAccess', 'delete'];

  constructor(
    private carService: CarService,
    private dialog: MatDialog
  ) {
  }

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;


  ngOnInit(): void {
    this.getAll();
  }

  private getAll(): void {
    this.carService.getAll().subscribe(
      c => {
        this.dataSource = new MatTableDataSource<Car>(c);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      }
    )
  }

  changeAccess(car: Car): void {
    this.carService.changeAccess(car).subscribe(
      c => {
        this.getAll();
      }
    )
  }

  deleteCar(car: Car): void {
    this.carService.delete(car).subscribe(
      c => {
        this.getAll();
      }
    )
  }

  public add(): void {
    const dialogRef = this.dialog.open(CarAddComponent, {
      height: '80%',
      width: '50%'
    })

    dialogRef.afterClosed().subscribe(_ => {
      this.getAll();
    });
  }

}
