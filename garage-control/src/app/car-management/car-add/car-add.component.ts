import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {CarService} from "../../car.service";
import {Car} from "../../model/car";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-car-add',
  templateUrl: './car-add.component.html',
  styleUrls: ['./car-add.component.css']
})
export class CarAddComponent implements OnInit {

  constructor(
    private carService: CarService,
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<CarAddComponent>
  ) {
  }

  form!: FormGroup;

  ngOnInit(): void {
    this.form = this.formBuilder.group(
      {
        licensePlate: ['', [Validators.required]],
        width: [[Validators.required]],
        length: [[Validators.required]],
        hasAccess: [[Validators.required]]
      }
    )
  }

  public save(): void {
    let car: Car = new Car;
    car.license_plate = this.form.value.licensePlate
    car.length = this.form.value.length;
    car.width = this.form.value.width;
    car.hasAccess = this.form.value.hasAccess;
    this.carService.addCar(car).subscribe(_ => {
        this.dialogRef.close();
      }
    )

  }

}
