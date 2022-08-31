package com.example.robotcatmobile.home_parts;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.R;

import java.util.ArrayList;

/*
responsible for creating the grids with just
 */
public class GridRecycler extends RecyclerView.Adapter<GridRecycler.ViewHolder> {
    ArrayList<Button> arrayOfGridButtons = new ArrayList<>();

    public static final int COLUMNS = 20;

    public static final int ROWS = 20;

    // the array of grids
    public ViewHolder[] arrOfGrids = new ViewHolder[COLUMNS * ROWS];

    public GridRecycler() {
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.grid_button, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        // setting up the position
        holder.mY = position / ROWS;
        holder.mX = position % COLUMNS;
        // then we can just set the array of grids as it is
        arrOfGrids[position] = holder;
    }

    @Override
    public int getItemCount() {
        return COLUMNS * ROWS;
    }

    /*
    The individual buttons at the grid
     */
    class ViewHolder extends RecyclerView.ViewHolder {
        /*
         position along the x axis
         */
        public int mX;
        /*
        position along the y axis
         */
        public int mY;
        // the button of this view holder
        Button mGridButton;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            mGridButton = itemView.findViewById(R.id.grid_button);
            mGridButton.setOnClickListener(view -> {

            });
        }
    }
}
